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
from .simulator import Scheduler, Priority, Task


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
            # print(f"  📈 Task {task.id} elevated! (pressure={pressure:.2f} > {self.alpha})")
            return Priority.HIGH

        return Priority.LOW

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None

        # Sort by (effective_priority, deadline)
        # Dynamically elevated tasks compete equally with original high-priority
        return min(ready_tasks,
                  key=lambda t: (self.get_effective_priority(t).value, t.deadline))


class MaxMin_Scheduler(Scheduler):
    """
    Max-Min Fairness (Heuristic)

    Selects the task with the longest processing time among compatible tasks.
    In a cloud context, this can help clear large jobs when resources are available,
    preventing them from being delayed indefinitely by small jobs (fragmentation).
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        # Select the task with the maximum processing time (Longest Job First)
        return max(ready_tasks, key=lambda t: t.processing_time)


class FCFS_Scheduler(Scheduler):
    """
    First Come First Served (FCFS)

    Simple non-preemptive algorithm that schedules tasks in order of arrival.
    Fair but can lead to convoy effect (short tasks waiting for long ones).
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None
        # Select the task with the earliest arrival time
        # Tie-break with ID to ensure stability
        return min(ready_tasks, key=lambda t: (t.arrival_time, t.id))


class HRRN_Scheduler(Scheduler):
    """
    Highest Response Ratio Next (HRRN)

    Response Ratio = (Waiting Time + Service Time) / Service Time
                   = 1 + (Waiting Time / Service Time)

    Favors tasks that have waited longer, preventing starvation while still
    giving preference to shorter tasks.
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None

        def response_ratio(task: Task) -> float:
            waiting_time = self.current_time - task.arrival_time
            # Avoid division by zero if processing_time is 0 (though unlikely)
            service_time = max(task.processing_time, 0.0001)
            return (waiting_time + service_time) / service_time

        # Select task with highest response ratio
        return max(ready_tasks, key=response_ratio)


class MLF_Scheduler(Scheduler):
    """
    Minimum Laxity First (MLF)

    Laxity = (Deadline - Current Time) - Remaining Processing Time

    Selects the task with the least laxity (slack time).
    Optimal for real-time systems but can cause frequent context switches
    (though this simulator is non-preemptive per task execution).
    """

    def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
        if not ready_tasks:
            return None

        def get_laxity(task: Task) -> float:
            # For non-preemptive, remaining time is just processing time
            # since we only select tasks that haven't started.
            return (task.deadline - self.current_time) - task.processing_time

        # Select task with minimum laxity
        return min(ready_tasks, key=get_laxity)


# Algorithm registry for experiment runner
AVAILABLE_ALGORITHMS = {
    'SPT': SPT_Scheduler,
    'EDF': EDF_Scheduler,
    'Priority-First': PriorityFirst_Scheduler,
    'Max-Min (Cloud)': MaxMin_Scheduler,
    'DPE (α=0.3)': lambda t, m: DPE_Scheduler(t, m, alpha=0.3),
    'DPE (α=0.5)': lambda t, m: DPE_Scheduler(t, m, alpha=0.5),
    'DPE (α=0.7)': lambda t, m: DPE_Scheduler(t, m, alpha=0.7),
    'DPE (α=0.9)': lambda t, m: DPE_Scheduler(t, m, alpha=0.9),
    'FCFS': FCFS_Scheduler,
    'HRRN': HRRN_Scheduler,
    'MLF': MLF_Scheduler,
}


def get_all_algorithms() -> Dict[str, Type[Scheduler]]:
    """
    Get all available algorithms for experiments.

    Returns:
        dict: Algorithm name → Scheduler class or factory function
    """
    return AVAILABLE_ALGORITHMS.copy()
