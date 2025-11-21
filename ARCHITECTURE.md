# PySchedule Architecture

## System Overview

PySchedule is a discrete-event simulation framework for evaluating real-time scheduling algorithms. The system follows a modular architecture with clear separation of concerns across 5 core components.

### Design Philosophy

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Extensibility**: Easy to add new algorithms, scenarios, and metrics without modifying core code
3. **Reproducibility**: Deterministic simulation with fixed random seeds for repeatable experiments
4. **Performance**: Efficient algorithms (O(n log n) event processing) for large-scale experiments
5. **Research-First**: Designed for systematic algorithm comparison and rigorous evaluation

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│  (CLI / Python API / Jupyter Notebooks)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Experiment Runner                              │
│  • Orchestrates algorithm/scenario combinations                 │
│  • Collects performance metrics                                 │
│  • Manages parallel execution                                   │
└─────┬──────────────────────────────────────┬────────────────────┘
      │                                      │
      │                                      │
┌─────▼─────────────────┐           ┌───────▼────────────────────┐
│  Scheduling Algorithms │           │   Test Scenarios           │
│  • SPT                 │           │   • Simple (4)             │
│  • EDF                 │           │   • Challenge (5)          │
│  • Priority-First      │           │   • Extreme (5)            │
│  • DPE (5 variants)    │           │   • Advanced (5)           │
└─────┬─────────────────┘           │   • New (5)                │
      │                             └───────┬────────────────────┘
      │                                     │
┌─────▼─────────────────────────────────────▼────────────────────┐
│              Discrete-Event Simulation Engine                   │
│  • Task: arrival_time, processing_time, deadline, priority     │
│  • Machine: execution state tracking                           │
│  • Event: time-based simulation events (priority queue)        │
│  • Scheduler: base class with event loop                       │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          │ Results (completion times, tardiness)
                          │
┌─────────────────────────▼──────────────────────────────────────┐
│                   Visualization System                          │
│  • Gantt charts (task scheduling timelines)                    │
│  • Performance comparisons (algorithm evaluation)              │
│  • Pareto frontiers (fairness-efficiency trade-offs)           │
│  • Heatmaps (success rates by priority)                        │
└────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Discrete-Event Simulation Engine (`simple_simulator.py`)

**Purpose**: Provides the fundamental abstractions and event-driven simulation infrastructure.

#### Key Classes

##### Task
Represents a schedulable unit of work.

**Attributes**:
- `arrival_time`: When task enters system
- `processing_time`: CPU time required
- `deadline`: Must complete by this time
- `priority`: Static priority level (Priority.LOW, MEDIUM, HIGH)
- `task_id`: Unique identifier

**Methods**:
- `meets_deadline() -> bool`: Check if completed before deadline
- `deadline_pressure(current_time) -> float`: Calculate urgency (0.0 to 1.0)

**Design Rationale**: Tasks are immutable after creation to ensure reproducibility. The deadline_pressure() method enables dynamic priority calculations in adaptive algorithms.

##### Machine
Tracks execution state of a single processing unit.

**Attributes**:
- `machine_id`: Unique identifier
- `current_task`: Currently executing task (or None)
- `start_time`: When current task started
- `total_busy_time`: Cumulative execution time
- `task_history`: List of completed tasks

**Methods**:
- `is_idle(current_time) -> bool`: Check if machine is free
- `start_task(task, current_time)`: Begin task execution
- `complete_task(current_time)`: Finish current task

**Design Rationale**: Centralized machine state enables accurate utilization tracking and supports future multi-machine extensions.

##### Event
Represents a time-based simulation event.

**Attributes**:
- `time`: When event occurs
- `event_type`: "arrival" or "completion"
- `task`: Associated task
- `machine_id`: Machine involved (for completions)

**Ordering**: Events are ordered by time, with arrivals before completions at same time.

**Design Rationale**: Priority queue-based event processing (via heapq) ensures O(n log n) simulation performance.

##### Scheduler (Base Class)
Abstract base class defining the scheduling algorithm interface.

**Core Attributes**:
- `tasks`: List of all tasks to schedule
- `num_machines`: Number of available machines
- `machines`: List of Machine objects
- `event_queue`: Priority queue of events
- `current_time`: Simulation clock
- `results`: Performance metrics

**Core Methods**:
- `run()`: Execute simulation event loop
- `select_task() -> Task`: **Abstract method** - algorithm-specific task selection
- `handle_arrival(event)`: Process task arrival event
- `handle_completion(event)`: Process task completion event
- `print_results()`: Display performance metrics

**Event Loop**:
```python
def run(self):
    while self.event_queue:
        event = heapq.heappop(self.event_queue)
        self.current_time = event.time

        if event.event_type == "arrival":
            self.handle_arrival(event)
        elif event.event_type == "completion":
            self.handle_completion(event)

        # Assign waiting tasks to idle machines
        self.assign_tasks_to_machines()
```

**Design Rationale**: The Template Method pattern allows algorithm implementations to focus solely on task selection logic while inheriting all simulation infrastructure.

---

### 2. Scheduling Algorithms (`algorithms.py`)

**Purpose**: Implements 8 scheduling algorithm variants, each with different task selection strategies.

#### Algorithm Variants

##### SPT (Shortest Processing Time)
**Strategy**: Always select task with smallest processing_time
**Complexity**: O(n log n) with heap-based priority queue
**Characteristics**:
- Minimizes average completion time
- Ignores deadlines and priorities
- Baseline greedy algorithm

**Implementation**:
```python
def select_task(self) -> Task:
    return min(self.ready_tasks,
               key=lambda t: t.processing_time)
```

##### EDF (Earliest Deadline First)
**Strategy**: Always select task with earliest deadline
**Complexity**: O(n log n) with heap-based priority queue
**Characteristics**:
- Optimal for single machine (Liu & Layland 1973)
- Minimizes deadline misses
- Ignores processing time and priority

**Implementation**:
```python
def select_task(self) -> Task:
    return min(self.ready_tasks,
               key=lambda t: t.deadline)
```

##### Priority-First
**Strategy**: Select highest priority, break ties with EDF
**Complexity**: O(n log n) with heap-based priority queue
**Characteristics**:
- Respects static priority levels
- Uses EDF for fairness within priority class
- Can starve low-priority tasks

**Implementation**:
```python
def select_task(self) -> Task:
    return min(self.ready_tasks,
               key=lambda t: (-t.priority.value, t.deadline))
```

##### DPE (Dynamic Priority Elevation)
**Strategy**: Elevate priority based on deadline pressure when α threshold exceeded
**Parameters**: α ∈ {0.3, 0.5, 0.7, 0.9, 1.0}
**Complexity**: O(n log n) with heap-based priority queue
**Characteristics**:
- Balances static priority with deadline urgency
- Lower α = more responsive to deadlines (fairness)
- Higher α = more respect for priority (efficiency)
- α = 1.0 equivalent to Priority-First

**Implementation**:
```python
def select_task(self) -> Task:
    deadline_pressure = (self.current_time - t.arrival_time) / \
                       (t.deadline - t.arrival_time)

    if deadline_pressure >= self.alpha:
        # Elevate to highest priority
        effective_priority = Priority.HIGH
    else:
        effective_priority = t.priority

    return min(self.ready_tasks,
               key=lambda t: (-effective_priority.value,
                             t.deadline))
```

**Design Rationale**: DPE explores the fairness-efficiency trade-off space by parameterizing the urgency threshold. This allows systematic investigation of when to override static priorities.

#### Algorithm Factory

```python
def get_all_algorithms() -> Dict[str, Type[Scheduler]]:
    """Returns mapping of algorithm names to classes"""
    return {
        "SPT": SPT_Scheduler,
        "EDF": EDF_Scheduler,
        "Priority-First": PriorityFirst_Scheduler,
        "DPE-0.3": lambda tasks, machines: DPE_Scheduler(tasks, machines, alpha=0.3),
        "DPE-0.5": lambda tasks, machines: DPE_Scheduler(tasks, machines, alpha=0.5),
        "DPE-0.7": lambda tasks, machines: DPE_Scheduler(tasks, machines, alpha=0.7),
        "DPE-0.9": lambda tasks, machines: DPE_Scheduler(tasks, machines, alpha=0.9),
        "DPE-1.0": lambda tasks, machines: DPE_Scheduler(tasks, machines, alpha=1.0),
    }
```

---

### 3. Test Scenarios (`scenarios.py`)

**Purpose**: Defines 24 standardized workload scenarios for systematic algorithm evaluation.

#### Scenario Structure

```python
scenario = {
    "name": "Scenario Name",
    "tasks": [
        {
            "arrival_time": 0.0,
            "processing_time": 2.0,
            "deadline": 10.0,
            "priority": "HIGH"
        },
        # ... more tasks
    ],
    "num_machines": 2
}
```

#### Scenario Categories

1. **Simple (4 scenarios)**: Basic validation - small task sets, obvious optimal solutions
2. **Challenge (5 scenarios)**: Algorithm differentiation - designed to expose trade-offs
3. **Extreme (5 scenarios)**: Stress tests - high load, tight deadlines, edge cases
4. **Advanced (5 scenarios)**: Realistic workloads - multi-machine, mixed priorities
5. **New (5 scenarios)**: Alpha sensitivity - systematic DPE parameter exploration

**Design Rationale**: Hierarchical scenario organization enables progressive evaluation:
- Simple scenarios validate correctness
- Challenge scenarios differentiate algorithms
- Extreme scenarios test robustness
- Advanced scenarios simulate real-world conditions
- New scenarios explore parameter sensitivity

#### Scenario Factory

```python
def get_all_scenarios() -> List[Dict]:
    """Returns all 24 test scenarios"""
    return [
        simple_scenario_1(),
        simple_scenario_2(),
        # ... 22 more scenarios
    ]
```

---

### 4. Experiment Runner (`runner.py`)

**Purpose**: Orchestrates systematic evaluation of all algorithm/scenario combinations.

#### ExperimentRunner Class

**Core Functionality**:
```python
class ExperimentRunner:
    def __init__(self):
        self.algorithms = get_all_algorithms()
        self.scenarios = get_all_scenarios()
        self.results = []

    def run_all_experiments(self):
        """Execute all combinations (8 algorithms × 24 scenarios = 192 experiments)"""
        for scenario in self.scenarios:
            for algo_name, algo_class in self.algorithms.items():
                result = self.run_experiment(scenario, algo_name, algo_class)
                self.results.append(result)

        return self.results

    def run_experiment(self, scenario, algo_name, algo_class):
        """Single algorithm/scenario execution with metric collection"""
        scheduler = algo_class(scenario["tasks"], scenario["num_machines"])
        scheduler.run()

        return {
            "scenario": scenario["name"],
            "algorithm": algo_name,
            "total_tardiness": scheduler.total_tardiness,
            "missed_deadlines": scheduler.missed_deadlines,
            "completion_time": scheduler.current_time,
            "task_results": scheduler.results
        }
```

**Parallel Execution Support** (future):
```python
def run_all_experiments_parallel(self, num_workers=4):
    """Parallel execution using multiprocessing"""
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.starmap(self.run_experiment,
                              self.generate_experiment_configs())
    return results
```

**Design Rationale**: Centralized experiment orchestration ensures:
- Consistent execution across all combinations
- Standardized metric collection
- Easy addition of new algorithms/scenarios
- Support for future parallelization

---

### 5. Visualization System (`visualizer.py`)

**Purpose**: Generates publication-quality visualizations for research analysis.

#### SchedulingVisualizer Class

**Visualization Types**:

1. **Gantt Charts**: Task scheduling timelines
   - X-axis: Time
   - Y-axis: Machines
   - Color: Task priority
   - Shows: Execution order, idle time, priority distribution

2. **Algorithm Performance Comparison**: Comparative metrics
   - Tardiness by algorithm
   - Deadline success rates
   - Completion times
   - Enables: Algorithm selection, trade-off analysis

3. **Pareto Frontier Analysis**: Fairness-efficiency trade-offs
   - X-axis: Total tardiness (efficiency)
   - Y-axis: Priority unfairness (fairness)
   - Points: Algorithm configurations
   - Shows: Non-dominated solutions

4. **Performance Heatmaps**: Success rates by priority
   - Rows: Algorithms
   - Columns: Priority levels
   - Color: Success rate percentage
   - Shows: Priority-specific performance

5. **Alpha Sensitivity Analysis**: DPE parameter exploration
   - X-axis: Alpha values (0.3 to 1.0)
   - Y-axis: Performance metrics
   - Shows: Parameter impact on outcomes

**Output Configuration**:
- Format: PNG (300 DPI for publication quality)
- Size: 10×6 inches (standard paper width)
- Style: Clean, minimal, color-blind friendly
- Location: `./output/` directory

**Design Rationale**: Visualization-first design enables:
- Rapid insight generation from raw metrics
- Publication-ready figures without manual editing
- Systematic comparison across algorithms
- Clear communication of research findings

---

## Data Flow

### End-to-End Execution Pipeline

```
1. Scenario Definition (scenarios.py)
   └─> scenario = {"name": "...", "tasks": [...], "num_machines": 2}

2. Experiment Orchestration (runner.py)
   └─> for each (scenario, algorithm) combination:

3. Scheduler Initialization
   └─> scheduler = Algorithm(tasks, num_machines)

4. Simulation Execution (simple_simulator.py)
   └─> while event_queue not empty:
       ├─> pop next event
       ├─> update simulation time
       ├─> handle event (arrival/completion)
       └─> assign tasks to idle machines via select_task()

5. Metric Collection
   └─> results = {
       "total_tardiness": ...,
       "missed_deadlines": ...,
       "completion_time": ...,
       "task_results": [...]
   }

6. Visualization Generation (visualizer.py)
   └─> create_gantt_chart(scheduler, ...)
   └─> create_performance_comparison(results, ...)
   └─> create_pareto_frontier(results, ...)
```

### State Management

**Simulation State**:
- `current_time`: Simulation clock (float)
- `event_queue`: Pending events (heapq)
- `ready_tasks`: Tasks awaiting execution (list)
- `machines`: Machine states (list of Machine objects)
- `completed_tasks`: Finished tasks (list)

**Invariants**:
1. `current_time` always equals time of last processed event
2. All events in queue have time ≥ current_time
3. No task can be in multiple states (ready/running/completed) simultaneously
4. Machine.current_task is None iff machine is idle

---

## Performance Characteristics

### Time Complexity

| Component | Operation | Complexity | Rationale |
|-----------|-----------|------------|-----------|
| Event Queue | Insert event | O(log n) | Binary heap (heapq) |
| Event Queue | Pop min | O(log n) | Binary heap |
| Task Selection | Find next task | O(n log n) | Priority-based selection |
| Simulation | Complete run | O(n log n) | n events, log n per event |
| Total Experiment | All scenarios | O(n² log n) | 192 runs × O(n log n) each |

**Bottleneck**: Task selection in tight event loops. Future optimization: maintain sorted task queues.

### Space Complexity

| Component | Space Usage | Scaling |
|-----------|-------------|---------|
| Task Storage | O(n) | n = number of tasks |
| Event Queue | O(n) | Max 2n events (arrivals + completions) |
| Machine State | O(m) | m = number of machines |
| Results | O(n) | One result per task |
| Visualizations | O(n) | Matplotlib memory for n tasks |

**Total**: O(n + m) per experiment, O(192(n + m)) for full suite.

### Scalability Limits

**Current Implementation**:
- Tasks: Tested up to 100 tasks per scenario
- Machines: Tested up to 5 machines
- Scenarios: 24 scenarios × 8 algorithms = 192 experiments
- Total Runtime: ~5-10 seconds on modern hardware

**Scaling Considerations**:
- 1000+ tasks: Consider C++ implementation or Cython
- 10+ machines: May need specialized data structures
- 100+ scenarios: Parallel execution recommended

---

## Extension Points

### Adding Custom Algorithms

**Step 1**: Inherit from Scheduler base class
```python
from simple_simulator import Scheduler, Task

class CustomScheduler(Scheduler):
    def __init__(self, tasks, num_machines, custom_param=0.5):
        super().__init__(tasks, num_machines)
        self.custom_param = custom_param

    def select_task(self) -> Task:
        # Implement custom task selection logic
        # Must return a Task from self.ready_tasks
        return my_custom_selection_logic()
```

**Step 2**: Register in algorithm factory
```python
def get_all_algorithms():
    return {
        # ... existing algorithms
        "Custom": CustomScheduler,
    }
```

**Requirements**:
- Must implement `select_task() -> Task`
- Must return task from `self.ready_tasks`
- Can access `self.current_time`, `self.machines`, `self.completed_tasks`
- Should be deterministic for reproducibility

### Adding Custom Scenarios

**Format**:
```python
def custom_scenario():
    return {
        "name": "Custom Workload",
        "tasks": [
            {
                "arrival_time": 0.0,      # When task arrives
                "processing_time": 5.0,   # CPU time required
                "deadline": 20.0,         # Must complete by
                "priority": "HIGH"        # LOW, MEDIUM, or HIGH
            },
            # ... more tasks
        ],
        "num_machines": 2
    }
```

**Best Practices**:
- Use realistic arrival patterns (Poisson, batch, periodic)
- Ensure feasibility: sum(processing_time) ≤ num_machines × max(deadline)
- Mix priority levels for interesting trade-offs
- Document scenario intent and expected algorithm behavior

### Adding Custom Metrics

**Step 1**: Extend metric collection in Scheduler
```python
class Scheduler:
    def calculate_metrics(self):
        # Existing metrics
        self.total_tardiness = sum(task.tardiness for task in self.completed_tasks)

        # Add custom metric
        self.custom_metric = self.calculate_custom_metric()

    def calculate_custom_metric(self):
        # Your custom metric logic
        return computed_value
```

**Step 2**: Update visualization
```python
def plot_custom_metric(results):
    custom_values = [r["custom_metric"] for r in results]
    # Generate visualization
```

### Adding Custom Visualizations

```python
class SchedulingVisualizer:
    def create_custom_plot(self, data, title, filename):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Your custom plotting logic
        ax.plot(data)

        plt.title(title)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
```

---

## Design Principles

### 1. Separation of Concerns
- **Simulation Engine**: Core abstractions, event loop, state management
- **Algorithms**: Task selection policies only
- **Scenarios**: Workload definitions only
- **Runner**: Experiment orchestration only
- **Visualizer**: Presentation only

**Benefits**: Easy to modify one component without affecting others.

### 2. Open/Closed Principle
- **Open for Extension**: Add algorithms via inheritance, add scenarios via factory
- **Closed for Modification**: Core simulation engine unchanged when adding features

**Benefits**: System grows without breaking existing functionality.

### 3. Dependency Inversion
- Algorithms depend on Scheduler abstraction, not concrete implementation
- Runner depends on algorithm interface, not specific algorithms
- Visualizer depends on result structure, not execution details

**Benefits**: Loose coupling enables independent testing and development.

### 4. Single Responsibility
- Each class has one reason to change
- Task: represent work
- Machine: track execution
- Event: represent time point
- Scheduler: coordinate simulation
- Algorithm: select next task

**Benefits**: Clear boundaries, easy to understand and maintain.

### 5. Composition Over Inheritance
- Machine composed of Task references, not inheriting from Task
- Scheduler composed of Machines, not inheriting from Machine
- Results composed of metric dicts, not complex class hierarchies

**Benefits**: Flexible relationships, avoid deep inheritance trees.

---

## Testing Strategy

### Unit Tests
- **Task**: deadline_pressure() calculation, meets_deadline() logic
- **Machine**: state transitions, idle detection
- **Scheduler**: event processing, metric calculation
- **Algorithms**: task selection correctness for known inputs

### Integration Tests
- **End-to-End**: Run simple scenarios, verify expected outcomes
- **Algorithm Comparison**: Ensure relative performance matches theory
- **Reproducibility**: Same random seed produces identical results

### Property-Based Tests
- **Event Ordering**: All events processed in time order
- **Task Completion**: All tasks eventually complete or are marked missed
- **Machine Utilization**: Never idle while tasks waiting (work-conserving)
- **Fairness**: Higher priority tasks not starved indefinitely

### Regression Tests
- **Benchmark Scenarios**: Track performance over code changes
- **Visualization**: Ensure charts remain publication-quality

---

## Future Enhancements

### Short-Term (Sprints 2-4)
- Type hints for static analysis
- Comprehensive docstrings
- CLI interface for easy execution
- Configuration file support
- Package setup (pip installable)

### Medium-Term
- Multi-machine load balancing algorithms
- Task migration between machines
- Preemptive scheduling variants
- Real-time constraint violations
- Interactive visualization (Plotly)

### Long-Term
- Distributed system simulation
- Energy-aware scheduling
- Machine learning-based algorithms
- Online learning and adaptation
- Cloud deployment optimization

---

## References

### Foundational Theory
- Liu, C.L. & Layland, J.W. (1973). "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment"
- Buttazzo, G. (2011). "Hard Real-Time Computing Systems"

### Design Patterns
- Gamma et al. (1994). "Design Patterns: Elements of Reusable Object-Oriented Software"
- Martin, R. (2017). "Clean Architecture"

### Discrete-Event Simulation
- Law, A.M. (2015). "Simulation Modeling and Analysis"
- Banks et al. (2010). "Discrete-Event System Simulation"

---

**Last Updated**: 2024
**Version**: 1.0
**Authors**: PySchedule Development Team
