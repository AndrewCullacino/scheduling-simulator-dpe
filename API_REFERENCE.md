# PySchedule API Reference

Complete API documentation for all classes, methods, and functions in PySchedule.

---

## Table of Contents

- [Core Classes](#core-classes)
  - [Task](#task)
  - [Priority](#priority)
  - [Machine](#machine)
  - [Event](#event)
  - [Scheduler](#scheduler-base-class)
- [Algorithm Implementations](#algorithm-implementations)
  - [SPT_Scheduler](#spt_scheduler)
  - [EDF_Scheduler](#edf_scheduler)
  - [PriorityFirst_Scheduler](#priorityfirst_scheduler)
  - [DPE_Scheduler](#dpe_scheduler)
- [Experiment Runner](#experiment-runner)
  - [ExperimentRunner](#experimentrunner)
- [Utility Functions](#utility-functions)
  - [get_all_algorithms](#get_all_algorithms)
  - [get_all_scenarios](#get_all_scenarios)
  - [run_all_experiments](#run_all_experiments)

---

## Core Classes

### Task

Represents a schedulable unit of work with timing constraints and priority.

**Module**: `simple_simulator.py`

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique task identifier |
| `arrival_time` | `float` | Time when task enters the system |
| `processing_time` | `float` | CPU time required to complete task |
| `priority` | `Priority` | Task priority level (HIGH or LOW) |
| `deadline` | `float` | Time by which task must complete |
| `start_time` | `Optional[float]` | Actual start time (set during simulation) |
| `completion_time` | `Optional[float]` | Actual completion time (set during simulation) |
| `machine_id` | `Optional[int]` | Machine assignment (set during simulation) |

#### Methods

##### `meets_deadline() -> bool`

Check if task completed before its deadline.

**Returns**: `True` if task completed on time, `False` otherwise

**Example**:
```python
task = Task(id=1, arrival_time=0, processing_time=5,
            priority=Priority.HIGH, deadline=20)
# After simulation
if task.meets_deadline():
    print(f"Task {task.id} completed on time")
```

##### `deadline_pressure(current_time: float) -> float`

Calculate deadline urgency for Dynamic Priority Elevation algorithm.

**Formula**: `time_elapsed / time_available`

**Parameters**:
- `current_time` (float): Current simulation time

**Returns**: `float` - Deadline pressure ratio (0.0 to inf)
- `0.0` if task already started
- `inf` if deadline already passed
- Fraction between 0 and 1 otherwise

**Example**:
```python
task = Task(id=1, arrival_time=0, processing_time=5,
            priority=Priority.LOW, deadline=20)

# At time 10
pressure = task.deadline_pressure(10)  # Returns 10/20 = 0.5

# At time 25 (past deadline)
pressure = task.deadline_pressure(25)  # Returns inf
```

---

### Priority

Enumeration for task priority levels.

**Module**: `simple_simulator.py`

#### Values

| Value | Integer | Description |
|-------|---------|-------------|
| `Priority.HIGH` | 1 | High-priority task |
| `Priority.LOW` | 2 | Low-priority task |

**Example**:
```python
from simple_simulator import Priority

high_task = Task(..., priority=Priority.HIGH)
low_task = Task(..., priority=Priority.LOW)

# Compare priorities
if task.priority == Priority.HIGH:
    print("High priority task")
```

---

### Machine

Represents a processing machine resource.

**Module**: `simple_simulator.py`

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Unique machine identifier |
| `available_at` | `float` | Time when machine becomes available |

#### Methods

##### `is_idle(current_time: float) -> bool`

Check if machine is available at given time.

**Parameters**:
- `current_time` (float): Time to check availability

**Returns**: `True` if machine is idle, `False` otherwise

**Example**:
```python
machine = Machine(id=0, available_at=5.0)

if machine.is_idle(current_time=10.0):  # Returns True
    # Assign task to machine
    machine.available_at = current_time + task.processing_time
```

---

### Event

Represents a time-based simulation event.

**Module**: `simple_simulator.py`

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `time` | `float` | When event occurs |
| `event_type` | `str` | "arrival" or "completion" |
| `task` | `Task` | Associated task |
| `machine_id` | `Optional[int]` | Machine involved (for completions) |

**Ordering**: Events are ordered by time, with arrivals before completions at same time.

**Example**:
```python
# Events are managed internally by Scheduler
# Users typically don't create events directly
arrival = Event(time=0.0, event_type="arrival",
                task=task, machine_id=None)
```

---

### Scheduler (Base Class)

Abstract base class defining the scheduling algorithm interface.

**Module**: `simple_simulator.py`

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `tasks` | `List[Task]` | All tasks to schedule |
| `num_machines` | `int` | Number of available machines |
| `machines` | `List[Machine]` | Machine objects |
| `event_queue` | `List[Event]` | Priority queue of events |
| `current_time` | `float` | Simulation clock |
| `results` | `List[Task]` | Completed tasks with metrics |
| `total_tardiness` | `float` | Sum of all task tardiness |
| `missed_deadlines` | `int` | Count of missed deadlines |

#### Abstract Methods

##### `select_task(ready_tasks: List[Task]) -> Optional[Task]`

**MUST BE IMPLEMENTED BY SUBCLASSES**

Select the next task to execute from ready queue.

**Parameters**:
- `ready_tasks` (`List[Task]`): Tasks waiting for execution

**Returns**: `Optional[Task]` - Selected task or None if no tasks ready

**Example**:
```python
class CustomScheduler(Scheduler):
    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        # Custom selection logic
        return min(ready_tasks, key=lambda t: t.deadline)
```

#### Methods

##### `run() -> None`

Execute the discrete-event simulation.

**Process**:
1. Initialize event queue with all task arrivals
2. While events remain:
   - Pop next event
   - Update simulation time
   - Handle event (arrival/completion)
   - Assign waiting tasks to idle machines
3. Calculate final metrics

**Example**:
```python
scheduler = SPT_Scheduler(tasks, num_machines=2)
scheduler.run()

print(f"Simulation completed at time: {scheduler.current_time}")
print(f"Total tardiness: {scheduler.total_tardiness}")
print(f"Missed deadlines: {scheduler.missed_deadlines}")
```

##### `handle_arrival(event: Event) -> None`

Process task arrival event (called internally by `run()`).

**Parameters**:
- `event` (Event): Arrival event to process

##### `handle_completion(event: Event) -> None`

Process task completion event (called internally by `run()`).

**Parameters**:
- `event` (Event): Completion event to process

##### `assign_tasks_to_machines() -> None`

Assign waiting tasks to idle machines using `select_task()` (called internally by `run()`).

##### `print_results() -> None`

Display simulation results in formatted table.

**Output**:
- Task ID, arrival time, start time, completion time
- Deadline, met/missed status, tardiness
- Summary: total tardiness, missed deadlines, success rate

**Example**:
```python
scheduler.run()
scheduler.print_results()

# Output:
# Task Results:
# Task 1: [0.0 → 0.0 → 5.0] Deadline: 20.0 ✓ (Tardiness: 0.0)
# Task 2: [5.0 → 5.0 → 12.0] Deadline: 15.0 ✓ (Tardiness: 0.0)
# ...
```

---

## Algorithm Implementations

### SPT_Scheduler

Shortest Processing Time First scheduler.

**Module**: `algorithms.py`

**Strategy**: Always select task with smallest processing_time

**Characteristics**:
- Minimizes average completion time
- Ignores deadlines and priorities
- Baseline greedy algorithm
- Optimal for minimizing mean flow time

**Complexity**: O(n) per task selection

#### Constructor

```python
SPT_Scheduler(tasks: List[Task], num_machines: int)
```

**Parameters**:
- `tasks` (`List[Task]`): Tasks to schedule
- `num_machines` (`int`): Number of machines available

#### Methods

##### `select_task(ready_tasks: List[Task]) -> Optional[Task]`

Select task with shortest processing time.

**Returns**: Task with minimum `processing_time`, or `None` if queue empty

**Example**:
```python
from simple_simulator import Task, Priority
from algorithms import SPT_Scheduler

tasks = [
    Task(id=1, arrival_time=0, processing_time=10,
         priority=Priority.HIGH, deadline=50),
    Task(id=2, arrival_time=0, processing_time=5,
         priority=Priority.LOW, deadline=20),
]

scheduler = SPT_Scheduler(tasks, num_machines=1)
scheduler.run()
scheduler.print_results()
```

**Use Cases**:
- Minimizing average response time
- Batch processing systems
- When deadlines don't matter

---

### EDF_Scheduler

Earliest Deadline First scheduler.

**Module**: `algorithms.py`

**Strategy**: Always select task with earliest deadline

**Characteristics**:
- Optimal for single-machine scheduling (Liu & Layland 1973)
- Minimizes deadline misses when feasible
- Ignores processing time and priority
- Dynamic priority based on deadline urgency

**Complexity**: O(n) per task selection

#### Constructor

```python
EDF_Scheduler(tasks: List[Task], num_machines: int)
```

**Parameters**:
- `tasks` (`List[Task]`): Tasks to schedule
- `num_machines` (`int`): Number of machines available

#### Methods

##### `select_task(ready_tasks: List[Task]) -> Optional[Task]`

Select task with earliest deadline.

**Returns**: Task with minimum `deadline`, or `None` if queue empty

**Example**:
```python
from algorithms import EDF_Scheduler

scheduler = EDF_Scheduler(tasks, num_machines=2)
scheduler.run()

# EDF will prioritize tasks by deadline urgency
# Guaranteed optimal for single-machine systems
```

**Use Cases**:
- Real-time systems with hard deadlines
- Single-machine scheduling
- When deadline compliance is critical

---

### PriorityFirst_Scheduler

Static Priority scheduling with EDF tiebreaking.

**Module**: `algorithms.py`

**Strategy**: Select highest priority, break ties with EDF

**Characteristics**:
- Respects static priority levels
- Uses EDF for fairness within priority class
- Can cause low-priority task starvation
- Simple and predictable behavior

**Complexity**: O(n) per task selection

#### Constructor

```python
PriorityFirst_Scheduler(tasks: List[Task], num_machines: int)
```

**Parameters**:
- `tasks` (`List[Task]`): Tasks to schedule
- `num_machines` (`int`): Number of machines available

#### Methods

##### `select_task(ready_tasks: List[Task]) -> Optional[Task]`

Select highest priority task, use deadline for tiebreaking.

**Sort Key**: `(priority.value, deadline)`
- Priority.HIGH = 1, Priority.LOW = 2
- Lower values selected first

**Returns**: Highest priority task (earliest deadline if tied), or `None` if queue empty

**Example**:
```python
from algorithms import PriorityFirst_Scheduler

scheduler = PriorityFirst_Scheduler(tasks, num_machines=2)
scheduler.run()

# All HIGH priority tasks execute before LOW priority
# Within same priority: earliest deadline first
```

**Use Cases**:
- Systems with strict priority requirements
- Mission-critical vs best-effort workloads
- When priority must never be violated

**Trade-offs**:
- ✅ Guarantees priority respect
- ❌ Can starve low-priority tasks indefinitely

---

### DPE_Scheduler

Dynamic Priority Elevation scheduler with configurable α threshold.

**Module**: `algorithms.py`

**Strategy**: Elevate priority based on deadline pressure when α threshold exceeded

**Characteristics**:
- Balances static priority with deadline urgency
- Configurable α parameter controls trade-off
- Lower α = more responsive to deadlines (fairness)
- Higher α = more respect for priority (efficiency)
- α = 1.0 equivalent to Priority-First

**Complexity**: O(n) per task selection

#### Constructor

```python
DPE_Scheduler(tasks: List[Task], num_machines: int, alpha: float = 0.7)
```

**Parameters**:
- `tasks` (`List[Task]`): Tasks to schedule
- `num_machines` (`int`): Number of machines available
- `alpha` (`float`, optional): Elevation threshold (default: 0.7)
  - Range: 0.0 to 1.0
  - α ≤ 0.5: Conservative elevation (prevents starvation)
  - α > 0.5: Aggressive elevation (permits starvation)

#### Methods

##### `get_effective_priority(task: Task) -> Priority`

Calculate effective priority with dynamic elevation.

**Logic**:
1. If task has HIGH priority → return HIGH
2. Calculate deadline pressure: `(current_time - arrival_time) / (deadline - arrival_time)`
3. If pressure > α → elevate to HIGH
4. Otherwise → keep LOW

**Parameters**:
- `task` (`Task`): Task to evaluate

**Returns**: `Priority.HIGH` (original or elevated) or `Priority.LOW` (not elevated)

**Example**:
```python
scheduler = DPE_Scheduler(tasks, num_machines=2, alpha=0.5)

# At time 10, task with deadline 20, arrival 0
# Pressure = 10/20 = 0.5
# If pressure > 0.5: elevate to HIGH
```

##### `select_task(ready_tasks: List[Task]) -> Optional[Task]`

Select task based on effective priority and deadline.

**Sort Key**: `(effective_priority.value, deadline)`

**Returns**: Task with highest effective priority (earliest deadline if tied), or `None` if queue empty

**Example**:
```python
from algorithms import DPE_Scheduler

# Conservative: prevents starvation
scheduler_conservative = DPE_Scheduler(tasks, num_machines=2, alpha=0.3)
scheduler_conservative.run()

# Aggressive: permits starvation for efficiency
scheduler_aggressive = DPE_Scheduler(tasks, num_machines=2, alpha=0.9)
scheduler_aggressive.run()
```

#### Research Findings

**Pareto Optimal Configurations** (from empirical analysis):
- **α = 0.3, 0.5**: Achieve 71.4% low-priority success rate
- **α = 0.7, 0.9**: Achieve 42.9% low-priority success rate

**Recommendation**: Use α ≤ 0.5 for fairness-critical systems

**Use Cases**:
- Mixed-criticality real-time systems
- Preventing priority inversion
- Balancing SLA requirements across priority levels

---

## Experiment Runner

### ExperimentRunner

Orchestrates systematic evaluation of all algorithm/scenario combinations.

**Module**: `runner.py`

#### Constructor

```python
ExperimentRunner()
```

**Attributes**:
- `results` (`List[Dict[str, Any]]`): Collected metrics from all experiments
- `best_makespan_per_scenario` (`Dict[str, float]`): Best makespan for normalization

#### Methods

##### `run_experiment(scenario: Dict[str, Any], algorithm_name: str, SchedulerClass: Type[Scheduler], **kwargs: Any) -> Dict[str, Any]`

Run single experiment and collect metrics.

**Parameters**:
- `scenario` (`Dict`): Scenario definition with tasks and machines
- `algorithm_name` (`str`): Name of algorithm for reporting
- `SchedulerClass` (`Type[Scheduler]`): Scheduler class or factory function
- `**kwargs`: Additional arguments for scheduler initialization

**Returns**: `Dict` - Metrics dictionary with performance measurements

**Metrics Returned**:
- `Scenario`: Scenario name
- `Algorithm`: Algorithm name
- `Total Tasks`: Number of tasks
- `High Priority Tasks`: Count of HIGH priority tasks
- `Low Priority Tasks`: Count of LOW priority tasks
- `High Met Deadline`: HIGH tasks meeting deadline
- `Low Met Deadline`: LOW tasks meeting deadline
- `Total Met Deadline`: Total tasks meeting deadline
- `High Success Rate (%)`: HIGH task success percentage
- `Low Success Rate (%)`: LOW task success percentage
- `Total Success Rate (%)`: Overall success percentage
- `Makespan`: Total completion time
- `Composite Performance Score (%)`: Harmonic mean of success and efficiency
- `Avg Response Time`: Average (completion - arrival)
- `Avg Waiting Time`: Average (start - arrival)
- `Simulation Time`: Final simulation clock

**Example**:
```python
from runner import ExperimentRunner
from algorithms import get_all_algorithms
from scenarios import get_all_scenarios

runner = ExperimentRunner()
scenarios = get_all_scenarios()
algorithms = get_all_algorithms()

metrics = runner.run_experiment(
    scenario=scenarios[0],
    algorithm_name="DPE (α=0.5)",
    SchedulerClass=algorithms['DPE (α=0.5)']
)

print(f"Success Rate: {metrics['Total Success Rate (%)']:.1f}%")
```

##### `calculate_metrics(tasks: List[Task], scenario_name: str, algorithm_name: str, sim_time: float) -> Dict[str, Any]`

Calculate comprehensive performance metrics (called internally by `run_experiment`).

**Parameters**:
- `tasks` (`List[Task]`): Tasks after simulation
- `scenario_name` (`str`): Name of scenario
- `algorithm_name` (`str`): Name of algorithm
- `sim_time` (`float`): Final simulation time

**Returns**: `Dict` - Complete metrics dictionary

##### `calculate_composite_scores() -> None`

Calculate composite performance scores after all experiments.

**Formula**: Harmonic mean (F-score) of success rate and makespan efficiency
- Success Rate: percentage of tasks meeting deadlines
- Makespan Efficiency: `(best_makespan / current_makespan) × 100`
- Composite Score: `2 × (SR × ME) / (SR + ME)`

**Rationale**: Penalizes imbalanced performance, prevents gaming single metric

**Example**:
```python
runner = ExperimentRunner()

# Run all experiments
for scenario in scenarios:
    for name, scheduler in algorithms.items():
        runner.run_experiment(scenario, name, scheduler)

# Calculate composite scores
runner.calculate_composite_scores()

# Now results have meaningful composite scores
```

##### `export_to_csv(filename: str = 'results/experiment_results.csv') -> None`

Export all results to CSV file.

**Parameters**:
- `filename` (`str`, optional): Output CSV path (default: results/experiment_results.csv)

**Example**:
```python
runner.export_to_csv('results/my_experiments.csv')
# Creates results/ directory if needed
# Exports all metrics to CSV for analysis
```

##### `compare_algorithms() -> None`

Print formatted comparison table across all scenarios.

**Output**: Console table grouped by scenario with columns:
- Algorithm name
- Success percentage
- High priority success
- Low priority success
- Makespan

**Example**:
```python
runner.compare_algorithms()

# Output:
# ========================================
# COMPARISON TABLE
# ========================================
#
# Simple Scenario 1:
# ------------------------------------
# Algorithm          | Success% | High% | Low%  | Makespan
# ------------------------------------
# SPT                | 85.7     | 100.0 | 71.4  | 45.0
# EDF                | 92.9     | 100.0 | 85.7  | 47.2
# ...
```

---

## Utility Functions

### get_all_algorithms

Get all available scheduling algorithms.

**Module**: `algorithms.py`

**Signature**:
```python
def get_all_algorithms() -> Dict[str, Type[Scheduler]]
```

**Returns**: `Dict[str, Type[Scheduler]]` - Mapping of algorithm names to scheduler classes/factories

**Available Algorithms**:
- `'SPT'`: SPT_Scheduler
- `'EDF'`: EDF_Scheduler
- `'Priority-First'`: PriorityFirst_Scheduler
- `'DPE (α=0.3)'`: DPE_Scheduler with α=0.3
- `'DPE (α=0.5)'`: DPE_Scheduler with α=0.5
- `'DPE (α=0.7)'`: DPE_Scheduler with α=0.7
- `'DPE (α=0.9)'`: DPE_Scheduler with α=0.9

**Example**:
```python
from algorithms import get_all_algorithms

algorithms = get_all_algorithms()

# Create scheduler instance
spt = algorithms['SPT'](tasks, num_machines=2)

# DPE requires factory function call
dpe_05 = algorithms['DPE (α=0.5)'](tasks, num_machines=2)
```

---

### get_all_scenarios

Get all test scenarios.

**Module**: `scenarios.py`

**Signature**:
```python
def get_all_scenarios() -> List[Dict[str, Any]]
```

**Returns**: `List[Dict]` - List of 24 scenario definitions

**Scenario Structure**:
```python
{
    "name": "Scenario Name",
    "description": "Scenario description",
    "tasks": [
        {
            "id": 1,
            "arrival_time": 0.0,
            "processing_time": 5.0,
            "priority": "HIGH",  # or "LOW"
            "deadline": 20.0
        },
        # ... more tasks
    ],
    "num_machines": 2
}
```

**Scenario Categories** (24 total):
- **Simple (4)**: Basic validation scenarios
- **Challenge (5)**: Algorithm differentiation tests
- **Extreme (5)**: Stress tests and edge cases
- **Advanced (5)**: Realistic multi-machine workloads
- **New (5)**: Alpha sensitivity exploration

**Example**:
```python
from scenarios import get_all_scenarios

scenarios = get_all_scenarios()
print(f"Total scenarios: {len(scenarios)}")  # 24

# Run specific scenario
simple_1 = scenarios[0]
print(f"Scenario: {simple_1['name']}")
print(f"Tasks: {len(simple_1['tasks'])}")
print(f"Machines: {simple_1['num_machines']}")
```

---

### run_all_experiments

Run complete experimental suite.

**Module**: `runner.py`

**Signature**:
```python
def run_all_experiments() -> None
```

**Process**:
1. Create ExperimentRunner
2. Get all 24 scenarios
3. Get all 7 algorithms
4. Run 168 experiments (24 × 7)
5. Calculate composite scores
6. Print comparison table
7. Export to CSV

**Output**:
- Console progress and results
- `results/comprehensive_results.csv` file

**Example**:
```python
from runner import run_all_experiments

# Run complete experimental suite
run_all_experiments()

# Output:
# ╔══════════════════════════════════════════╗
# ║   RUNNING COMPREHENSIVE EXPERIMENTS      ║
# ║   Total Scenarios: 24 | Algorithms: 7   ║
# ╚══════════════════════════════════════════╝
#
# 🔬 Running: SPT on Simple Scenario 1
#   ✓ Success Rate: 85.7%
#   ✓ High Priority: 100.0%
#   ✓ Low Priority: 71.4%
#   ⏱ Makespan: 45.0
# ...
# ✅ ALL EXPERIMENTS COMPLETE!
# Results saved to: results/comprehensive_results.csv
```

---

## Type Definitions

### Common Type Aliases

```python
from typing import List, Optional, Dict, Type, Any

TaskList = List[Task]
ScenarioDict = Dict[str, Any]
AlgorithmRegistry = Dict[str, Type[Scheduler]]
MetricsDict = Dict[str, Any]
```

---

## Error Handling

### Common Errors

**ValueError**: Invalid algorithm parameters
```python
# alpha must be between 0 and 1
scheduler = DPE_Scheduler(tasks, num_machines=2, alpha=1.5)  # Raises ValueError
```

**IndexError**: Empty task list
```python
scheduler = SPT_Scheduler([], num_machines=2)
scheduler.run()  # May raise IndexError
```

**TypeError**: Invalid task structure
```python
# Tasks must have all required fields
invalid_task = {"arrival_time": 0}  # Missing required fields
```

---

## Best Practices

### Creating Tasks

```python
# ✅ Good: Use Priority enum
from simple_simulator import Task, Priority

task = Task(
    id=1,
    arrival_time=0.0,
    processing_time=5.0,
    priority=Priority.HIGH,
    deadline=20.0
)

# ❌ Bad: Don't use string/int directly
task = Task(..., priority="HIGH")  # Wrong type
task = Task(..., priority=1)       # Wrong type
```

### Running Simulations

```python
# ✅ Good: Make copies if running multiple algorithms
import copy
from algorithms import SPT_Scheduler, EDF_Scheduler

original_tasks = [...]

# SPT run
spt_tasks = copy.deepcopy(original_tasks)
spt = SPT_Scheduler(spt_tasks, num_machines=2)
spt.run()

# EDF run (separate copy)
edf_tasks = copy.deepcopy(original_tasks)
edf = EDF_Scheduler(edf_tasks, num_machines=2)
edf.run()

# ❌ Bad: Reuse same task list
scheduler1 = SPT_Scheduler(tasks, 2)
scheduler1.run()
scheduler2 = EDF_Scheduler(tasks, 2)  # Tasks already modified!
scheduler2.run()
```

### Extending Algorithms

```python
# ✅ Good: Inherit from Scheduler, implement select_task
from simple_simulator import Scheduler, Task
from typing import List, Optional

class CustomScheduler(Scheduler):
    def __init__(self, tasks: List[Task], num_machines: int,
                 custom_param: float = 0.5) -> None:
        super().__init__(tasks, num_machines)
        self.custom_param = custom_param

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        # Custom logic here
        return min(ready_tasks, key=self.custom_scoring_function)

    def custom_scoring_function(self, task: Task) -> float:
        return task.processing_time * self.custom_param

# ❌ Bad: Don't directly subclass built-in algorithms
class MyEDF(EDF_Scheduler):  # Fragile inheritance
    pass
```

---

## Version History

- **v1.0** (2024): Initial API documentation
  - Core classes: Task, Priority, Machine, Event, Scheduler
  - Algorithms: SPT, EDF, Priority-First, DPE (5 variants)
  - Experiment infrastructure: ExperimentRunner, utilities
  - 24 test scenarios across 5 categories
  - Type hints for all core modules

---

**Maintained by**: PySchedule Development Team
**Last Updated**: 2024
**License**: MIT
