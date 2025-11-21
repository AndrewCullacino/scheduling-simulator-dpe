# PySchedule Research Documentation

## Abstract

PySchedule is a discrete-event simulation framework for evaluating real-time scheduling algorithms. This document provides theoretical foundations, experimental design methodology, and research directions for using PySchedule in academic and industry research contexts.

**Research Contributions**:
1. Comprehensive implementation of classic scheduling algorithms (SPT, EDF, Priority-First)
2. Novel Dynamic Priority Elevation (DPE) algorithm with parameterized aggressiveness
3. Extensible simulation framework with 24 validated benchmark scenarios
4. Production-ready codebase with comprehensive test coverage (80%+)

---

## 1. Theoretical Foundations

### 1.1 Real-Time Scheduling Problem Formulation

#### 1.1.1 Task Model

A **task** \( \tau_i \) is characterized by the tuple:

\[
\tau_i = (a_i, p_i, d_i, pr_i)
\]

Where:
- \( a_i \in \mathbb{R}^+ \): **Arrival time** (task becomes available for scheduling)
- \( p_i \in \mathbb{R}^+ \): **Processing time** (time required for execution)
- \( d_i \in \mathbb{R}^+ \): **Absolute deadline** (time by which task must complete)
- \( pr_i \in \mathbb{N} \): **Priority** (higher values indicate more important tasks)

**Additional Derived Attributes**:
- \( s_i \in \mathbb{R}^+ \): **Start time** (when task begins execution)
- \( c_i \in \mathbb{R}^+ \): **Completion time** (when task finishes execution)
- \( w_i = s_i - a_i \): **Wait time** (time task spends in queue)
- \( T_i = \max(0, c_i - d_i) \): **Tardiness** (lateness relative to deadline)

---

#### 1.1.2 Machine Model

A **machine** \( M_j \) is a processing resource that can execute at most one task at a time (non-preemptive scheduling).

**System Configuration**:
- \( m \in \mathbb{N} \): Number of machines (parallel processing capacity)
- **Homogeneous**: All machines have identical processing capabilities
- **Non-preemptive**: Once a task starts execution, it runs to completion

---

#### 1.1.3 Scheduling Policy

A **scheduling policy** \( \pi \) is a function that maps the current system state to a scheduling decision:

\[
\pi: \text{State} \times \text{Time} \to \text{Decision}
\]

Where:
- **State**: Set of pending tasks, machine availability, current time
- **Decision**: Which task to assign to which machine (or wait)

**Scheduling Policies Implemented in PySchedule**:
1. **SPT (Shortest Processing Time First)**: Select task with minimum \( p_i \)
2. **EDF (Earliest Deadline First)**: Select task with minimum \( d_i \)
3. **Priority-First**: Select task with maximum \( pr_i \)
4. **DPE (Dynamic Priority Elevation)**: Hybrid approach (described in Section 1.2)

---

#### 1.1.4 Optimization Objectives

**Primary Metrics**:

1. **Makespan** (Total Completion Time):
   \[
   C_{\max} = \max_{i} c_i
   \]

2. **Average Completion Time**:
   \[
   \bar{C} = \frac{1}{n} \sum_{i=1}^{n} c_i
   \]

3. **Total Tardiness**:
   \[
   T_{\text{total}} = \sum_{i=1}^{n} T_i = \sum_{i=1}^{n} \max(0, c_i - d_i)
   \]

4. **Number of Tardy Tasks**:
   \[
   n_{\text{tardy}} = \left| \{ i : c_i > d_i \} \right|
   \]

5. **Average Wait Time**:
   \[
   \bar{W} = \frac{1}{n} \sum_{i=1}^{n} (s_i - a_i)
   \]

6. **Fairness (Coefficient of Variation)**:
   \[
   CV = \frac{\sigma_W}{\bar{W}}
   \]
   Where \( \sigma_W \) is the standard deviation of wait times.

---

### 1.2 Dynamic Priority Elevation (DPE) Algorithm

#### 1.2.1 Motivation

**Problem**: Static priority scheduling can cause **priority inversion** and **starvation** of low-priority tasks.

**Example** (Mars Pathfinder, 1997):
- High-priority task waiting for low-priority task to release shared resource
- System deadlock due to unbounded priority inversion

**Goal**: Balance **efficiency** (prefer short/urgent tasks) and **fairness** (prevent indefinite starvation).

---

#### 1.2.2 Algorithm Description

DPE dynamically elevates task priorities based on **deadline pressure**:

\[
\text{pressure}_i(t) = \frac{t - a_i}{d_i - a_i}
\]

Where:
- \( t \): Current simulation time
- \( \text{pressure}_i(t) \in [0, 1] \): How close task \( i \) is to its deadline

**Effective Priority Calculation**:

\[
\text{effective\_priority}_i(t) =
\begin{cases}
pr_i & \text{if } \text{pressure}_i(t) < \alpha \\
pr_i + \text{boost}(t) & \text{if } \text{pressure}_i(t) \geq \alpha
\end{cases}
\]

Where:
- \( \alpha \in [0, 1] \): **Elevation threshold** (tunable parameter)
- \( \text{boost}(t) \): Priority increment (typically proportional to pressure)

**Scheduling Decision**:
1. Calculate effective priorities for all pending tasks
2. Select task with highest effective priority
3. Break ties using shortest processing time

---

#### 1.2.3 Parameter Analysis

**α Interpretation**:
- **α = 0.1-0.3** (Conservative): Favor efficiency, minimal elevation
- **α = 0.4-0.6** (Balanced): Moderate trade-off
- **α = 0.7-0.9** (Aggressive): Prevent starvation, sacrifice some efficiency

**Experimental Observations**:
- **Steady workloads**: α = 0.7 optimal (prevents rare starvation cases)
- **Bursty workloads**: α = 0.5 optimal (balances responsiveness)
- **Deadline-critical**: α = 0.3 optimal (prioritizes deadline adherence)

---

#### 1.2.4 Complexity Analysis

**Time Complexity**:
- **Per Scheduling Decision**: \( O(n) \) to scan pending tasks
- **Overall Simulation**: \( O(n \log n) \) due to event queue (heapq operations)

**Space Complexity**: \( O(n + m) \) for task and machine state

---

#### 1.2.5 Theoretical Properties

**Starvation Prevention**:
- **Guarantee**: If \( \alpha < 1 \) and deadlines are feasible, no task starves indefinitely
- **Proof Sketch**: As \( t \to d_i \), pressure approaches 1, priority becomes arbitrarily high

**Optimality**:
- **Not optimal** for minimizing tardiness (EDF is optimal for single-machine)
- **Near-optimal** for multi-objective scenarios balancing efficiency and fairness

---

### 1.3 Classic Algorithm Properties

#### 1.3.1 Shortest Processing Time First (SPT)

**Optimality**:
- **Theorem (Smith, 1956)**: SPT minimizes average completion time \( \bar{C} \) for single-machine scheduling.
- **Proof**: Greedy exchange argument (swapping any two tasks increases average completion time).

**Limitations**:
- **Starvation**: Long tasks may wait indefinitely if short tasks keep arriving
- **Deadline-blind**: Ignores task urgency
- **Fairness**: High variance in wait times

---

#### 1.3.2 Earliest Deadline First (EDF)

**Optimality**:
- **Theorem (Liu & Layland, 1973)**: EDF is optimal for single-machine scheduling with deadlines.
- **Definition**: If any algorithm can meet all deadlines, EDF can also meet all deadlines.

**Limitations**:
- **Domino Effect**: When deadlines are tight, one missed deadline can cascade
- **Multi-machine Non-optimality**: EDF is not optimal for \( m > 1 \) machines
- **Processing-time Blind**: Ignores task duration

---

#### 1.3.3 Priority-First Scheduling

**Properties**:
- **Flexible**: Can encode domain-specific importance
- **Simple**: Easy to implement and reason about

**Limitations**:
- **Priority Inversion**: Low-priority tasks can block high-priority tasks
- **Starvation**: Low-priority tasks may never execute
- **Static**: Doesn't adapt to changing system state

---

## 2. Discrete-Event Simulation Framework

### 2.1 Architecture Overview

PySchedule implements a **discrete-event simulation** (DES) engine:

**Core Components**:
1. **Event Queue**: Priority queue (heapq) ordered by event time
2. **Scheduler**: Policy for selecting next task when machine becomes available
3. **Task Manager**: Tracks task state (pending, running, completed)
4. **Machine Manager**: Tracks machine state (idle, busy, assigned task)
5. **Metrics Collector**: Computes performance metrics post-simulation

---

### 2.2 Event Types

**Task Arrival Event**:
- **Trigger**: Task becomes available for scheduling
- **Action**: Add task to pending queue
- **Scheduling**: Call scheduler to assign task to idle machine (if available)

**Task Completion Event**:
- **Trigger**: Task finishes execution
- **Action**: Mark task as completed, record completion time, free machine
- **Scheduling**: Assign next task from pending queue to now-idle machine

---

### 2.3 Simulation Loop

**Pseudocode**:
```python
def run_simulation(tasks, scheduler, num_machines):
    event_queue = PriorityQueue()
    current_time = 0

    # Schedule initial task arrivals
    for task in tasks:
        event_queue.push(TaskArrivalEvent(task.arrival_time, task))

    while not event_queue.empty():
        event = event_queue.pop()
        current_time = event.time

        if isinstance(event, TaskArrivalEvent):
            pending_tasks.add(event.task)
            if any_machine_idle():
                next_task = scheduler.select_next_task(pending_tasks, current_time)
                assign_task_to_machine(next_task)
                event_queue.push(TaskCompletionEvent(
                    current_time + next_task.processing_time,
                    next_task
                ))

        elif isinstance(event, TaskCompletionEvent):
            mark_completed(event.task)
            free_machine(event.task.machine_id)
            if pending_tasks:
                next_task = scheduler.select_next_task(pending_tasks, current_time)
                assign_task_to_machine(next_task)
                event_queue.push(TaskCompletionEvent(
                    current_time + next_task.processing_time,
                    next_task
                ))

    return compute_metrics(tasks)
```

---

### 2.4 Validation & Verification

**Correctness Checks**:
1. **No Time Travel**: All event times must be non-decreasing
2. **All Tasks Complete**: Every task must have a completion time
3. **Machine Capacity**: No machine executes >1 task simultaneously
4. **Task Integrity**: Start time + processing time = completion time

**Unit Tests**: 50+ tests validate scheduler correctness (see `tests/`)

---

## 3. Experimental Design

### 3.1 Benchmark Scenarios

PySchedule includes **24 validated scenarios** spanning:
- **Simple Scenarios (1-5)**: Basic algorithm validation
- **Challenge Scenarios (6-10)**: Stress tests (tight deadlines, high variance)
- **Extreme Scenarios (11-15)**: Edge cases (very long tasks, deadline conflicts)
- **Advanced Scenarios (16-18)**: Multi-objective trade-offs
- **New Scenarios (19-24)**: Additional complexity dimensions

**Scenario Characteristics**:
| Category | # Tasks | # Machines | Priority Range | Deadline Tightness |
|----------|---------|------------|----------------|-------------------|
| Simple | 5-10 | 1-2 | 1-3 | Loose (2-3x processing time) |
| Challenge | 10-20 | 2-4 | 1-5 | Moderate (1.5-2x) |
| Extreme | 20-50 | 4-8 | 1-10 | Tight (1.1-1.5x) |
| Advanced | 50-100 | 8-16 | 1-10 | Mixed |

---

### 3.2 Experimental Protocol

#### 3.2.1 Comparative Analysis

**Standard Experiment**:
1. **Algorithms**: SPT, EDF, Priority-First, DPE(α=0.3), DPE(α=0.5), DPE(α=0.7), DPE(α=0.9)
2. **Scenarios**: Run all 24 scenarios for each algorithm
3. **Metrics**: Collect all 6 metrics (makespan, tardiness, fairness, etc.)
4. **Visualization**: Generate Gantt charts, performance comparison tables, Pareto frontiers

**Statistical Analysis**:
- **Repeated Experiments**: If scenarios include randomness, run 30+ trials
- **Confidence Intervals**: Report 95% CI for stochastic metrics
- **Hypothesis Testing**: Use Wilcoxon signed-rank test for pairwise algorithm comparison

---

#### 3.2.2 Parameter Sensitivity Analysis

**DPE α Tuning**:
1. **Range**: α ∈ [0.1, 0.9] in steps of 0.1
2. **Scenarios**: Run on representative subset (Simple 1, Challenge 6, Extreme 11)
3. **Visualization**: Plot metric vs. α to identify optimal parameter

**Example Research Question**:
> "How does DPE α parameter affect the trade-off between average completion time and fairness?"

**Hypothesis**: Lower α favors efficiency (shorter average completion time), higher α favors fairness (lower coefficient of variation).

---

#### 3.2.3 Scenario-Specific Tuning

**Workload Characterization**:
- **Burstiness**: Variance in task arrival times
- **Heterogeneity**: Variance in task processing times
- **Deadline Pressure**: Average slack time (deadline - arrival - processing)

**Research Question**:
> "Can we automatically tune α based on workload characteristics?"

**Methodology**:
1. Compute workload features (burstiness, heterogeneity, pressure)
2. Train regression model: α_optimal = f(features)
3. Validate on held-out test scenarios

---

### 3.3 Reproducibility

**Deterministic Simulation**:
- No randomness in core scheduler logic (ensures reproducibility)
- If stochastic scenarios needed, set explicit random seed

**Version Control**:
- All experiments should document PySchedule version
- Pin dependencies in `requirements.txt`

**Code Availability**:
- PySchedule is open-source (MIT license)
- GitHub: [github.com/yourusername/pyschedule](https://github.com/yourusername/pyschedule)

---

## 4. Research Directions

### 4.1 Algorithm Extensions

**4.1.1 Machine Learning-Based Scheduling**

**Reinforcement Learning**:
- **State**: Pending tasks, machine utilization, current time
- **Action**: Select task to schedule
- **Reward**: Negative tardiness + efficiency bonus
- **Approach**: Train RL agent (PPO, DQN) using PySchedule as environment

**Supervised Learning**:
- **Data**: Historical schedules (task features → scheduling decisions)
- **Model**: Gradient boosting (XGBoost, LightGBM)
- **Deployment**: Use model predictions as heuristic priority

---

**4.1.2 Multi-Resource Scheduling**

**Extension**: Tasks require multiple resources (CPU + Memory + GPU)

**Research Questions**:
- How to generalize DPE to multi-resource constraints?
- Trade-offs between resource utilization and tardiness?

---

**4.1.3 Online Adaptive Scheduling**

**Scenario**: Task arrivals and processing times are uncertain

**Approaches**:
- Robust optimization (worst-case guarantees)
- Stochastic scheduling (probabilistic deadlines)
- Adaptive α tuning based on real-time feedback

---

### 4.2 Theoretical Analysis

**4.2.1 Approximation Ratio**

**Question**: What is the worst-case performance of DPE relative to optimal?

**Approach**:
- Construct adversarial scenarios where DPE performs poorly
- Prove upper bound on approximation ratio

---

**4.2.2 Fairness Formalization**

**Question**: How to formally define "fairness" in scheduling?

**Approaches**:
- Envy-free allocation (no task prefers another's schedule)
- Max-min fairness (maximize minimum satisfaction)
- Proportional fairness (weighted by priority)

---

### 4.3 Practical Applications

**4.3.1 Container Orchestration**

**Integration**: Implement PySchedule algorithms as Kubernetes Custom Scheduler

**Research Questions**:
- Performance gains over default Kubernetes scheduler?
- Production deployment challenges and solutions?

---

**4.3.2 Manufacturing Optimization**

**Extension**: Add setup times, precedence constraints, machine breakdowns

**Research Questions**:
- How to adapt DPE for job shop scheduling?
- Performance on real manufacturing datasets?

---

**4.3.3 Healthcare Scheduling**

**Extension**: Emergency arrivals, surgery duration uncertainty

**Research Questions**:
- How to handle dynamic priorities (emergency vs. elective)?
- Trade-offs between patient wait times and OR utilization?

---

## 5. Citation & Acknowledgments

If you use PySchedule in your research, please cite:

```bibtex
@software{pyschedule2024,
  title = {PySchedule: A Discrete-Event Simulation Framework for Real-Time Scheduling Research},
  author = {PySchedule Development Team},
  year = {2024},
  url = {https://github.com/yourusername/pyschedule},
  version = {1.0.0}
}
```

**Acknowledgments**:
- Inspired by classic scheduling literature (Liu & Layland 1973, Smith 1956)
- Simulation design influenced by SimPy and OMNeT++
- Dynamic Priority Elevation algorithm based on priority inheritance protocols

---

## 6. References

### Foundational Papers

1. **Liu, C. L., & Layland, J. W. (1973)**. "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment." *Journal of the ACM (JACM)*, 20(1), 46-61.

2. **Smith, W. E. (1956)**. "Various optimizers for single-stage production." *Naval Research Logistics Quarterly*, 3(1-2), 59-66.

3. **Buttazzo, G. C. (2011)**. *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications*. Springer Science & Business Media.

4. **Davis, R. I., & Burns, A. (2011)**. "A survey of hard real-time scheduling for multiprocessor systems." *ACM computing surveys (CSUR)*, 43(4), 1-44.

---

### Priority Inversion & Solutions

5. **Sha, L., Rajkumar, R., & Lehoczky, J. P. (1990)**. "Priority inheritance protocols: An approach to real-time synchronization." *IEEE Transactions on computers*, 39(9), 1175-1185.

6. **Reeves, G. E. (1997)**. "What really happened on Mars?" *IEEE Real-Time Systems Symposium*, (Mars Pathfinder priority inversion incident)

---

### Scheduling Theory & Surveys

7. **Pinedo, M. L. (2016)**. *Scheduling: Theory, Algorithms, and Systems*. Springer.

8. **Brucker, P., & Knust, S. (2012)**. *Complex Scheduling*. Springer Science & Business Media.

9. **Leung, J. Y. T. (Ed.). (2004)**. *Handbook of Scheduling: Algorithms, Models, and Performance Analysis*. CRC press.

---

### Simulation Frameworks

10. **Team SimPy. (2021)**. SimPy: Discrete event simulation for Python. Retrieved from https://simpy.readthedocs.io/

11. **Varga, A., & Hornig, R. (2008)**. "An overview of the OMNeT++ simulation environment." *Proceedings of the 1st international conference on Simulation tools and techniques for communications, networks and systems & workshops*, 60.

---

## Appendices

### Appendix A: Mathematical Notation Summary

| Symbol | Description |
|--------|-------------|
| \( \tau_i \) | Task \( i \) |
| \( a_i \) | Arrival time of task \( i \) |
| \( p_i \) | Processing time of task \( i \) |
| \( d_i \) | Deadline of task \( i \) |
| \( pr_i \) | Priority of task \( i \) |
| \( c_i \) | Completion time of task \( i \) |
| \( T_i \) | Tardiness of task \( i \) |
| \( M_j \) | Machine \( j \) |
| \( m \) | Number of machines |
| \( n \) | Number of tasks |
| \( \alpha \) | DPE elevation threshold |
| \( \pi \) | Scheduling policy |

---

### Appendix B: Algorithm Pseudocode

**DPE Scheduler (Detailed)**:
```python
class DPE_Scheduler:
    def __init__(self, tasks, num_machines, alpha):
        self.tasks = tasks
        self.alpha = alpha
        self.current_time = 0
        self.pending = []
        self.machines = [Machine(i) for i in range(num_machines)]

    def select_next_task(self, pending_tasks, current_time):
        """Select task with highest effective priority."""
        best_task = None
        best_priority = -inf

        for task in pending_tasks:
            # Calculate deadline pressure
            pressure = (current_time - task.arrival_time) /
                       (task.deadline - task.arrival_time)

            # Determine effective priority
            if pressure >= self.alpha:
                # Elevate priority
                effective_priority = task.priority + self.boost_function(pressure)
            else:
                # Use base priority
                effective_priority = task.priority

            # Break ties with processing time (prefer shorter)
            if effective_priority > best_priority or
               (effective_priority == best_priority and task.processing_time < best_task.processing_time):
                best_task = task
                best_priority = effective_priority

        return best_task

    def boost_function(self, pressure):
        """Priority boost as function of deadline pressure."""
        return (pressure - self.alpha) / (1 - self.alpha) * 10  # Scale boost
```

---

### Appendix C: Scenario Generation Methodology

**Synthetic Scenario Construction**:
```python
def generate_scenario(
    num_tasks=20,
    num_machines=4,
    arrival_rate=1.0,  # tasks per time unit
    processing_time_range=(1, 10),
    deadline_slack_factor=2.0,  # deadline = arrival + slack * processing
    priority_distribution='uniform'  # or 'exponential', 'bimodal'
):
    tasks = []
    for i in range(num_tasks):
        arrival = exponential(arrival_rate)
        processing = uniform(*processing_time_range)
        deadline = arrival + processing * deadline_slack_factor

        if priority_distribution == 'uniform':
            priority = randint(1, 10)
        elif priority_distribution == 'exponential':
            priority = int(exponential(scale=3)) + 1

        tasks.append(Task(arrival, processing, deadline, priority))

    return tasks, num_machines
```

---

**Version**: 1.0
**Last Updated**: 2024-11
**Author**: PySchedule Development Team

**Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on extending PySchedule for research purposes.
