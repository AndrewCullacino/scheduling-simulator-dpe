"""
Scheduling Algorithm Implementations
====================================

All scheduling algorithms consolidated in one file:
- SPT (Shortest Processing Time)
- EDF (Earliest Deadline First)
- Priority-First (Static Priority with EDF tie-breaking)
- DPE (Dynamic Priority Elevation with configurable α threshold)
"""

from typing import List, Optional, Dict, Type
from simple_simulator import Scheduler, Priority, Task


class SPT_Scheduler(Scheduler):
    """
    Shortest Processing Time First

    Greedy algorithm that always selects the task with shortest processing time.
    Optimizes for makespan but ignores deadlines and priorities.
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        return min(ready_tasks, key=lambda t: t.processing_time)


class EDF_Scheduler(Scheduler):
    """
    Earliest Deadline First

    Greedy algorithm that always selects the task with earliest deadline.
    Optimal for single-machine scheduling without priorities.
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        return min(ready_tasks, key=lambda t: t.deadline)


class PriorityFirst_Scheduler(Scheduler):
    """
    Static Priority Scheduling

    Always schedules high-priority tasks first, uses EDF for tie-breaking
    within the same priority class. Can cause low-priority starvation.
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None

        # Sort by (priority value, deadline)
        # Priority.HIGH = 1, Priority.LOW = 2, so HIGH comes first
        return min(ready_tasks, key=lambda t: (t.priority.value, t.deadline))


class DPE_Scheduler(Scheduler):
    """
    Dynamic Priority Elevation (DPE)

    Adaptive algorithm that elevates low-priority tasks to high priority
    when their deadline pressure exceeds threshold α.

    Deadline pressure = (time_elapsed) / (time_available)

    Parameters:
        alpha (float): Elevation threshold (0.0 to 1.0)
                      - α ≤ 0.5: Conservative elevation (prevents starvation)
                      - α > 0.5: Aggressive elevation (permits starvation)

    Research findings:
        - α = 0.3, 0.5: Pareto optimal (71.4% low-priority success)
        - α = 0.7, 0.9: Permits starvation (42.9% low-priority success)
    """

    def __init__(self, tasks: List[Task], num_machines: int, alpha: float = 0.7) -> None:
        super().__init__(tasks, num_machines)
        self.alpha = alpha

    def get_effective_priority(self, task: Task) -> Priority:
        """
        Calculate effective priority with dynamic elevation.

        Args:
            task: Task to evaluate

        Returns:
            Priority: HIGH (original or elevated) or LOW (not elevated)
        """
        if task.priority == Priority.HIGH:
            return Priority.HIGH

        # Calculate deadline pressure for low-priority tasks
        pressure = task.deadline_pressure(self.current_time)

        if pressure > self.alpha:
            print(f"  📈 Task {task.id} elevated! (pressure={pressure:.2f} > {self.alpha})")
            return Priority.HIGH

        return Priority.LOW

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None

        # Sort by (effective_priority, deadline)
        # Dynamically elevated tasks compete equally with original high-priority
        return min(ready_tasks,
                  key=lambda t: (self.get_effective_priority(t).value, t.deadline))


# Algorithm registry for experiment runner
AVAILABLE_ALGORITHMS = {
    'SPT': SPT_Scheduler,
    'EDF': EDF_Scheduler,
    'Priority-First': PriorityFirst_Scheduler,
    'DPE (α=0.3)': lambda t, m: DPE_Scheduler(t, m, alpha=0.3),
    'DPE (α=0.5)': lambda t, m: DPE_Scheduler(t, m, alpha=0.5),
    'DPE (α=0.7)': lambda t, m: DPE_Scheduler(t, m, alpha=0.7),
    'DPE (α=0.9)': lambda t, m: DPE_Scheduler(t, m, alpha=0.9),
}


def get_all_algorithms() -> Dict[str, Type[Scheduler]]:
    """
    Get all available algorithms for experiments.

    Returns:
        dict: Algorithm name → Scheduler class or factory function
    """
    return AVAILABLE_ALGORITHMS.copy()
