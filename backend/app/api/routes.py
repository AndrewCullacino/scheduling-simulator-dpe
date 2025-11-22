from fastapi import APIRouter, HTTPException
from typing import List, Dict
from ..core.simulator import Task, Priority
from ..core.algorithms import get_all_algorithms, DPE_Scheduler
from ..core.scenarios import get_all_scenarios
from ..models import schemas

router = APIRouter()

@router.get("/algorithms", response_model=List[schemas.AlgorithmInfo])
def get_algorithms():
    """Get list of available scheduling algorithms."""
    algos = get_all_algorithms()
    result = []
    for name, cls in algos.items():
        # Extract description from docstring
        doc = cls.__doc__.strip().split('\n')[0] if cls.__doc__ else "No description available"
        result.append(schemas.AlgorithmInfo(
            id=name,
            name=name,
            description=doc
        ))
    return result

@router.get("/scenarios", response_model=List[schemas.ScenarioInfo])
def get_scenarios():
    """Get list of built-in test scenarios."""
    scenarios = get_all_scenarios()
    result = []
    for s in scenarios:
        tasks_input = [
            schemas.TaskInput(
                id=t.id,
                arrival_time=t.arrival_time,
                processing_time=t.processing_time,
                priority=schemas.PriorityEnum[t.priority.name],
                deadline=t.deadline
            ) for t in s['tasks']
        ]
        result.append(schemas.ScenarioInfo(
            id=s['name'], # Using name as ID for now
            name=s['name'],
            description=s['description'],
            num_machines=s['num_machines'],
            tasks=tasks_input
        ))
    return result

@router.post("/simulate", response_model=schemas.SimulationResult)
def run_simulation(request: schemas.SimulationRequest):
    """Run a simulation with provided configuration."""
    
    # Convert input tasks to internal Task objects
    tasks = []
    for t in request.tasks:
        priority = Priority.HIGH if t.priority == schemas.PriorityEnum.HIGH else Priority.LOW
        tasks.append(Task(
            id=t.id,
            arrival_time=t.arrival_time,
            processing_time=t.processing_time,
            priority=priority,
            deadline=t.deadline
        ))
    
    # Get algorithm class
    algos = get_all_algorithms()
    
    # Handle DPE special case (alpha parameter)
    if request.algorithm.startswith("DPE"):
        # If the user selected a specific DPE preset from the list, use it
        if request.algorithm in algos:
             scheduler_factory = algos[request.algorithm]
             # Check if it's a lambda (factory) or class
             if isinstance(scheduler_factory, type):
                 scheduler = scheduler_factory(tasks, request.num_machines, alpha=request.alpha)
             else:
                 # It's a lambda from the dictionary, likely has fixed alpha
                 scheduler = scheduler_factory(tasks, request.num_machines)
        else:
            # Generic DPE request
            scheduler = DPE_Scheduler(tasks, request.num_machines, alpha=request.alpha)
    elif request.algorithm in algos:
        SchedulerClass = algos[request.algorithm]
        scheduler = SchedulerClass(tasks, request.num_machines)
    else:
        raise HTTPException(status_code=404, detail=f"Algorithm '{request.algorithm}' not found")
    
    # Run simulation
    logs = scheduler.run()
    results = scheduler.get_results()
    
    # Format response
    response_logs = [
        schemas.LogEntry(
            time=l["time"],
            event=l["event"],
            task_id=l.get("task_id"),
            machine_id=l.get("machine_id"),
            message=l["message"],
            completion_time=l.get("completion_time")
        ) for l in logs
    ]
    
    response_tasks = [
        schemas.TaskResult(
            id=t["id"],
            priority=t["priority"],
            arrival_time=t["arrival_time"],
            start_time=t["start_time"],
            completion_time=t["completion_time"],
            deadline=t["deadline"],
            meets_deadline=t["meets_deadline"],
            cpu_required=t["cpu_required"],
            ram_required=t["ram_required"]
        ) for t in results["tasks"]
    ]
    
    return schemas.SimulationResult(
        makespan=results["makespan"],
        total_tasks=results["total_tasks"],
        high_priority_stats=schemas.PriorityStats(**results["high_priority_stats"]),
        low_priority_stats=schemas.PriorityStats(**results["low_priority_stats"]),
        tasks=response_tasks,
        logs=response_logs
    )
