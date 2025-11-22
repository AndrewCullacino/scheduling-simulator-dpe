"""
Simple Discrete-Event Scheduler Simulator
Real-Time Scheduling with Dynamic Priority Elevation

A minimal discrete-event simulation engine for evaluating scheduling algorithms
with priorities and deadlines. Designed for clarity and extensibility.
"""

import copy
import heapq
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict


class Priority(Enum):
    HIGH = 1
    LOW = 2


@dataclass
class Task:
    """
    Task definition with scheduling state.

    Attributes:
        id: Unique task identifier
        arrival_time: Time when task becomes available
        processing_time: Time required to complete task
        priority: Task priority level (HIGH or LOW)
        deadline: Time by which task must complete
        start_time: Actual start time (set during simulation)
        completion_time: Actual completion time (set during simulation)
        machine_id: Machine assignment (set during simulation)
    """
    id: int
    arrival_time: float
    processing_time: float
    priority: Priority
    deadline: float

    # Scheduling state (filled during simulation)
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    machine_id: Optional[int] = None

    def meets_deadline(self) -> bool:
        """
        Check if task completed before deadline.

        Returns:
            True if task completed on time, False otherwise
        """
        if self.completion_time is None:
            return False
        return self.completion_time <= self.deadline

    def deadline_pressure(self, current_time: float) -> float:
        """
        Calculate deadline pressure for DPE algorithm.

        Formula: time_elapsed / time_available

        Args:
            current_time: Current simulation time

        Returns:
            Deadline pressure ratio (0.0 to inf)
            - 0.0 if already started
            - inf if deadline already passed
            - fraction between 0 and 1 otherwise
        """
        if self.start_time is not None:
            return 0.0  # Already started

        time_elapsed = current_time - self.arrival_time
        time_available = self.deadline - self.arrival_time

        if time_available <= 0:
            return float('inf')

        return time_elapsed / time_available


@dataclass
class Machine:
    """
    Processing machine resource.

    Attributes:
        id: Unique machine identifier
        available_at: Time when machine becomes available
    """
    id: int
    available_at: float = 0.0

    def is_idle(self, current_time: float) -> bool:
        """
        Check if machine is available at given time.

        Args:
            current_time: Time to check availability

        Returns:
            True if machine is idle, False if busy
        """
        return current_time >= self.available_at


class Event:
    """
    Discrete event for simulation queue.

    Attributes:
        time: Event occurrence time
        type: Event type ('ARRIVAL' or 'COMPLETION')
        task: Associated task (if any)
        machine: Associated machine (if any)
    """

    def __init__(self, time: float, event_type: str,
                 task: Optional[Task] = None,
                 machine: Optional[Machine] = None):
        self.time = time
        self.type = event_type  # 'ARRIVAL' or 'COMPLETION'
        self.task = task
        self.machine = machine

    def __lt__(self, other: 'Event') -> bool:
        """Compare events by time for priority queue ordering."""
        return self.time < other.time


class Scheduler:
    """
    Base discrete-event simulator for scheduling algorithms.

    Attributes:
        all_tasks: Complete list of tasks to schedule
        num_machines: Number of parallel machines
        machines: List of Machine instances
        event_queue: Priority queue of events
        ready_queue: Queue of ready-to-schedule tasks
        current_time: Current simulation time
        completed_tasks: List of completed tasks
    """

    def __init__(self, tasks: List[Task], num_machines: int):
        self.all_tasks = tasks
        self.num_machines = num_machines
        self.machines = [Machine(i) for i in range(num_machines)]
        self.event_queue: List[Event] = []
        self.ready_queue: List[Task] = []
        self.current_time = 0.0
        self.completed_tasks: List[Task] = []

    def initialize(self) -> None:
        """Setup initial arrival events for all tasks."""
        for task in self.all_tasks:
            heapq.heappush(self.event_queue,
                          Event(task.arrival_time, 'ARRIVAL', task))

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        """
        Select next task to schedule (override in subclasses).

        Args:
            ready_tasks: List of tasks available for scheduling

        Returns:
            Selected task or None if no valid selection

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Must implement task selection strategy")
    
    def run(self) -> List[Dict]:
        """
        Main simulation loop.

        Process events chronologically, scheduling tasks on available machines
        according to the algorithm's selection strategy.
        
        Returns:
            List of log messages describing the simulation events.
        """
        self.initialize()
        logs = []

        while self.event_queue or self.ready_queue:
            # Process ALL events at the current time before scheduling
            if self.event_queue:
                event = heapq.heappop(self.event_queue)
                self.current_time = event.time

                # Collect all events at this time
                events_at_current_time = [event]
                while self.event_queue and self.event_queue[0].time == self.current_time:
                    events_at_current_time.append(heapq.heappop(self.event_queue))

                # Process all arrivals first, then completions
                for evt in sorted(events_at_current_time, key=lambda e: (e.type != 'ARRIVAL', e.type)):
                    if evt.type == 'ARRIVAL':
                        self.ready_queue.append(evt.task)
                        logs.append({
                            "time": self.current_time,
                            "event": "ARRIVAL",
                            "task_id": evt.task.id,
                            "message": f"Task {evt.task.id} arrives"
                        })

                    elif evt.type == 'COMPLETION':
                        evt.machine.available_at = self.current_time
                        evt.task.completion_time = self.current_time
                        self.completed_tasks.append(evt.task)
                        logs.append({
                            "time": self.current_time,
                            "event": "COMPLETION",
                            "task_id": evt.task.id,
                            "machine_id": evt.machine.id,
                            "message": f"Task {evt.task.id} completes on Machine {evt.machine.id}"
                        })

            # Try to schedule ready tasks on idle machines
            new_logs = self.schedule_ready_tasks()
            logs.extend(new_logs)
            
        return logs

    def schedule_ready_tasks(self) -> List[Dict]:
        """Assign ready tasks to idle machines using selection strategy."""
        logs = []
        while self.ready_queue:
            # Find idle machine
            idle_machine = None
            for machine in self.machines:
                if machine.is_idle(self.current_time):
                    idle_machine = machine
                    break

            if idle_machine is None:
                break  # No idle machines

            # Select task using strategy
            selected_task = self.select_task(self.ready_queue)
            if selected_task is None:
                break

            # Schedule task on machine
            self.ready_queue.remove(selected_task)
            selected_task.start_time = self.current_time
            selected_task.machine_id = idle_machine.id

            completion_time = self.current_time + selected_task.processing_time
            idle_machine.available_at = completion_time

            # Add completion event
            heapq.heappush(self.event_queue,
                          Event(completion_time, 'COMPLETION',
                               selected_task, idle_machine))

            logs.append({
                "time": self.current_time,
                "event": "START",
                "task_id": selected_task.id,
                "machine_id": idle_machine.id,
                "completion_time": completion_time,
                "message": f"Task {selected_task.id} starts on Machine {idle_machine.id} (completes at {completion_time:.1f})"
            })
        return logs
    
    def get_results(self) -> Dict:
        """Return comprehensive simulation results."""
        makespan = max((t.completion_time for t in self.completed_tasks), default=0)

        high_priority = [t for t in self.all_tasks if t.priority == Priority.HIGH]
        low_priority = [t for t in self.all_tasks if t.priority == Priority.LOW]

        high_met = sum(1 for t in high_priority if t.meets_deadline())
        low_met = sum(1 for t in low_priority if t.meets_deadline())
        
        tasks_data = []
        for task in sorted(self.completed_tasks, key=lambda t: t.id):
            tasks_data.append({
                "id": task.id,
                "priority": task.priority.name,
                "arrival_time": task.arrival_time,
                "start_time": task.start_time,
                "completion_time": task.completion_time,
                "deadline": task.deadline,
                "meets_deadline": task.meets_deadline()
            })

        return {
            "makespan": makespan,
            "total_tasks": len(self.all_tasks),
            "high_priority_stats": {
                "total": len(high_priority),
                "met_deadline": high_met
            },
            "low_priority_stats": {
                "total": len(low_priority),
                "met_deadline": low_met
            },
            "tasks": tasks_data
        }