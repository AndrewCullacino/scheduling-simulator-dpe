"""
Simple Discrete-Event Scheduler Simulator
For COMP3821 Project: Greedy Scheduling with DPE and Deadlines

This is a MINIMAL simulator that you can understand and extend easily.
No external dependencies needed!
"""

import heapq
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    HIGH = 1
    LOW = 2


@dataclass
class Task:
    """Task definition"""
    id: int
    arrival_time: float
    processing_time: float
    priority: Priority
    deadline: float
    
    # Scheduling state (filled during simulation)
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    machine_id: Optional[int] = None
    
    def meets_deadline(self):
        if self.completion_time is None:
            return False
        return self.completion_time <= self.deadline
    
    def deadline_pressure(self, current_time):
        """Calculate DPE metric"""
        if self.start_time is not None:
            return 0.0  # Already started
        
        time_elapsed = current_time - self.arrival_time
        time_available = self.deadline - self.arrival_time
        
        if time_available <= 0:
            return float('inf')
        
        return time_elapsed / time_available


@dataclass 
class Machine:
    """Processing machine"""
    id: int
    available_at: float = 0.0
    
    def is_idle(self, current_time):
        return current_time >= self.available_at


class Event:
    """Discrete event"""
    def __init__(self, time, event_type, task=None, machine=None):
        self.time = time
        self.type = event_type  # 'ARRIVAL' or 'COMPLETION'
        self.task = task
        self.machine = machine
    
    def __lt__(self, other):
        return self.time < other.time


class Scheduler:
    """Base discrete-event simulator"""
    
    def __init__(self, tasks: List[Task], num_machines: int):
        self.all_tasks = tasks
        self.num_machines = num_machines
        self.machines = [Machine(i) for i in range(num_machines)]
        self.event_queue = []
        self.ready_queue = []
        self.current_time = 0.0
        self.completed_tasks = []
    
    def initialize(self):
        """Setup initial events"""
        for task in self.all_tasks:
            heapq.heappush(self.event_queue, 
                          Event(task.arrival_time, 'ARRIVAL', task))
    
    def select_task(self, ready_tasks):
        """
        OVERRIDE THIS METHOD to implement different strategies!
        Returns: task to schedule next
        """
        raise NotImplementedError("Must implement task selection strategy")
    
    def run(self):
        """Main simulation loop"""
        self.initialize()
        
        while self.event_queue or self.ready_queue:
            # Get next event
            if self.event_queue:
                event = heapq.heappop(self.event_queue)
                self.current_time = event.time
                
                if event.type == 'ARRIVAL':
                    self.ready_queue.append(event.task)
                    print(f"⏰ Time {self.current_time:.1f}: Task {event.task.id} arrives")
                
                elif event.type == 'COMPLETION':
                    event.machine.available_at = self.current_time
                    event.task.completion_time = self.current_time
                    self.completed_tasks.append(event.task)
                    print(f"✅ Time {self.current_time:.1f}: Task {event.task.id} completes on Machine {event.machine.id}")
            
            # Try to schedule ready tasks on idle machines
            self.schedule_ready_tasks()
    
    def schedule_ready_tasks(self):
        """Assign ready tasks to idle machines"""
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
            
            print(f"🔨 Time {self.current_time:.1f}: Task {selected_task.id} starts on Machine {idle_machine.id} (completes at {completion_time:.1f})")
    
    def print_results(self):
        """Print summary"""
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        makespan = max((t.completion_time for t in self.completed_tasks), default=0)
        
        high_priority = [t for t in self.all_tasks if t.priority == Priority.HIGH]
        low_priority = [t for t in self.all_tasks if t.priority == Priority.LOW]
        
        high_met = sum(1 for t in high_priority if t.meets_deadline())
        low_met = sum(1 for t in low_priority if t.meets_deadline())
        
        print(f"Makespan: {makespan:.1f}")
        print(f"Total tasks: {len(self.all_tasks)}")
        print(f"High priority tasks: {len(high_priority)} ({high_met} met deadline)")
        print(f"Low priority tasks: {len(low_priority)} ({low_met} met deadline)")
        
        print("\nTask Details:")
        for task in sorted(self.completed_tasks, key=lambda t: t.id):
            status = "✓" if task.meets_deadline() else "✗"
            print(f"  Task {task.id}: [{task.priority.name[0]}] "
                  f"arrive={task.arrival_time:.1f}, "
                  f"start={task.start_time:.1f}, "
                  f"complete={task.completion_time:.1f}, "
                  f"deadline={task.deadline:.1f} {status}")


# =============================================================================
# ALGORITHM IMPLEMENTATIONS
# =============================================================================

class SPT_Scheduler(Scheduler):
    """Shortest Processing Time First"""
    
    def select_task(self, ready_tasks):
        if not ready_tasks:
            return None
        return min(ready_tasks, key=lambda t: t.processing_time)


class EDF_Scheduler(Scheduler):
    """Earliest Deadline First"""
    
    def select_task(self, ready_tasks):
        if not ready_tasks:
            return None
        return min(ready_tasks, key=lambda t: t.deadline)


class PriorityFirst_Scheduler(Scheduler):
    """Static Priority: High priority first, then EDF within each class"""
    
    def select_task(self, ready_tasks):
        if not ready_tasks:
            return None
        
        # Sort by (priority, deadline)
        return min(ready_tasks, key=lambda t: (t.priority.value, t.deadline))


class DPE_Scheduler(Scheduler):
    """Dynamic Priority Elevation with threshold α = 0.7"""
    
    def __init__(self, tasks, num_machines, alpha=0.7):
        super().__init__(tasks, num_machines)
        self.alpha = alpha
    
    def get_effective_priority(self, task):
        """Check if low-priority task should be elevated"""
        if task.priority == Priority.HIGH:
            return Priority.HIGH
        
        # Check deadline pressure for low-priority tasks
        pressure = task.deadline_pressure(self.current_time)
        if pressure > self.alpha:
            print(f"  📈 Task {task.id} elevated! (pressure={pressure:.2f} > {self.alpha})")
            return Priority.HIGH
        
        return Priority.LOW
    
    def select_task(self, ready_tasks):
        if not ready_tasks:
            return None
        
        # Sort by (effective_priority, deadline)
        return min(ready_tasks, 
                  key=lambda t: (self.get_effective_priority(t).value, t.deadline))


# =============================================================================
# TEST SCENARIOS
# =============================================================================

def create_test_scenario_1():
    """Simple scenario: 3 high, 2 low priority tasks on 2 machines"""
    return [
        Task(1, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=10),
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=12),
        Task(3, arrival_time=1, processing_time=4, priority=Priority.HIGH, deadline=15),
        Task(4, arrival_time=0, processing_time=5, priority=Priority.LOW, deadline=25),
        Task(5, arrival_time=2, processing_time=6, priority=Priority.LOW, deadline=30),
    ]


def create_test_scenario_2():
    """Starvation test: Many high priority tasks that could starve low priority"""
    return [
        Task(1, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=8),
        Task(2, arrival_time=1, processing_time=2, priority=Priority.HIGH, deadline=10),
        Task(3, arrival_time=2, processing_time=2, priority=Priority.HIGH, deadline=12),
        Task(4, arrival_time=3, processing_time=2, priority=Priority.HIGH, deadline=14),
        Task(5, arrival_time=0, processing_time=3, priority=Priority.LOW, deadline=15),  # Will this starve?
        Task(6, arrival_time=1, processing_time=3, priority=Priority.LOW, deadline=18),
    ]


# =============================================================================
# MAIN: Run experiments
# =============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║     Simple Discrete-Event Scheduler - Ready to Use!          ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    scenarios = [
        ("Scenario 1: Basic", create_test_scenario_1(), 2),
        ("Scenario 2: Starvation Test", create_test_scenario_2(), 2),
    ]
    
    algorithms = [
        ("SPT", SPT_Scheduler),
        ("EDF", EDF_Scheduler),
        ("Priority-First", PriorityFirst_Scheduler),
        ("DPE (α=0.7)", DPE_Scheduler),
    ]
    
    for scenario_name, tasks, num_machines in scenarios:
        print("\n" + "=" * 70)
        print(f"  {scenario_name}")
        print("=" * 70)
        
        for algo_name, SchedulerClass in algorithms:
            print(f"\n>>> Running {algo_name} <<<")
            print("-" * 70)
            
            # Create fresh task copies (reset state)
            import copy
            tasks_copy = copy.deepcopy(tasks)
            
            # Run scheduler
            scheduler = SchedulerClass(tasks_copy, num_machines)
            scheduler.run()
            scheduler.print_results()
            
            print()
    
    print("\n" + "=" * 70)
    print("✨ All simulations complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Modify create_test_scenario_X() to add your own test cases")
    print("2. Implement variations of DPE (try different α values)")
    print("3. Add more metrics (response time, waiting time, fairness)")
    print("4. Export results to CSV for analysis")
    print("=" * 70)