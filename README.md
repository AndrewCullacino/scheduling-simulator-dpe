# PySchedule: Real-Time Scheduling Research Toolkit

## Overview

A discrete-event simulation framework for evaluating real-time scheduling algorithms with priorities and deadlines. The codebase is organized into 5 core modules with clear separation of concerns.

## File Structure

```
simulator/
├── simple_simulator.py  # Core simulation engine
├── algorithms.py        # All scheduling algorithms
├── scenarios.py         # All 24 test scenarios
├── runner.py            # Experiment execution
├── visualizer.py        # All visualizations
├── results/             # Experimental results (CSV)
└── visualizations/      # Generated charts (PNG)
```

## Core Files

### 1. `simple_simulator.py` - Core Simulation Engine

**Purpose**: Discrete-event simulation infrastructure

**Contents**:
- `Priority` enum (HIGH, LOW)
- `Task` dataclass with deadline checking and pressure calculation
- `Machine` dataclass for processing units
- `Event` class for discrete events (ARRIVAL, COMPLETION)
- `Scheduler` base class with event queue and simulation loop

**Usage**:
```python
from simple_simulator import Task, Priority, Scheduler
```

### 2. `algorithms.py` - Scheduling Algorithms

**Purpose**: All algorithm implementations in one place

**Contents**:
- `SPT_Scheduler` - Shortest Processing Time
- `EDF_Scheduler` - Earliest Deadline First
- `PriorityFirst_Scheduler` - Static priority with EDF tie-breaking
- `DPE_Scheduler` - Dynamic Priority Elevation (α-parameterized)

**Usage**:
```python
from algorithms import get_all_algorithms

algorithms = get_all_algorithms()
scheduler = algorithms['EDF'](tasks, num_machines)
scheduler.run()
```

### 3. `scenarios.py` - Test Scenarios

**Purpose**: All 24 experimental scenarios consolidated

**Contents**:
- **Basic Scenarios** (4): Light Load, Heavy Load, Batch Arrival, Starvation Test
- **Challenge Scenarios** (5): Long High-Priority, Mixed Deadlines, Cascading, Interleaved, Tight Deadlines
- **Extreme Scenarios** (5): Overload, Impossible Deadlines, SPT Fails, EDF Fails, Priority Starvation
- **Advanced Scenarios** (5): Deadline Clusters, Priority Imbalance, Variable Load, Sparse Arrivals, Deadline Spread
- **New Scenarios** (5): Deadline Gradient, Priority Waves, Tight Margins, Overload Recovery, Cascading Failures

**Usage**:
```python
from scenarios import get_all_scenarios

scenarios = get_all_scenarios()
print(f"Total scenarios: {len(scenarios)}")
```

### 4. `runner.py` - Experiment Execution

**Purpose**: Run experiments and collect metrics

**Contents**:
- `ExperimentRunner` class
  - `run_experiment()` - Execute single experiment
  - `calculate_metrics()` - Compute performance metrics
  - `export_to_csv()` - Save results to CSV
  - `compare_algorithms()` - Print comparison table
- `run_all_experiments()` - Execute complete experimental suite (168 experiments)

**Usage**:
```python
from runner import run_all_experiments

# Run all 24 scenarios × 7 algorithms = 168 experiments
run_all_experiments()
# Results saved to: results/comprehensive_results.csv
```

### 5. `visualizer.py` - Visualizations

**Purpose**: Generate all publication-quality charts

**Contents**:
- `SchedulingVisualizer` class
  - `create_gantt_chart()` - Task scheduling timeline
- Aggregate visualization functions:
  - `create_algorithm_performance_by_category()` - Performance comparison
  - `create_alpha_sensitivity_clean()` - DPE α threshold analysis
  - `create_performance_heatmap_clean()` - Scenario × Algorithm heatmap
  - `create_success_rate_by_priority()` - Priority-stratified analysis
  - `create_pareto_frontier_clean()` - Fairness vs efficiency trade-off
- `generate_all_gantt_charts()` - Generate all 168 Gantt charts
- `generate_all_aggregate_visualizations()` - Generate 5 aggregate charts

**Usage**:
```python
from visualizer import generate_all_gantt_charts, generate_all_aggregate_visualizations

# Generate all visualizations
generate_all_gantt_charts()
generate_all_aggregate_visualizations()
# Output: 173 PNG files in visualizations/
```

## Workflow

### Complete Experimental Pipeline

```python
# 1. Run experiments and collect data
python3 runner.py
# → Output: results/comprehensive_results.csv

# 2. Generate all visualizations
python3 visualizer.py
# → Output: visualizations/*.png (173 files)

# 3. Analyze results
# Open results/comprehensive_results.csv in Excel/Sheets
# View visualizations in visualizations/ folder
```

### Custom Experiments

```python
from simple_simulator import Task, Priority
from algorithms import EDF_Scheduler, DPE_Scheduler
from scenarios import get_all_scenarios
from runner import ExperimentRunner

# Create custom scenario
tasks = [
    Task(1, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=10),
    Task(2, arrival_time=1, processing_time=5, priority=Priority.LOW, deadline=15),
]

# Run with specific algorithm
scheduler = DPE_Scheduler(tasks, num_machines=2, alpha=0.5)
scheduler.run()
scheduler.print_results()
```

## Benefits of Consolidation

### Before (12 files)
```
simple_scenarios.py
challenge_scenarios.py
extreme_scenarios.py
advanced_scenarios.py
new_experiments.py
experiment_runner.py
generate_all_visualizations.py
generate_new_visualizations.py
visualizations.py
enhanced_visualizations.py
improved_visualizations.py
simple_simulator.py
```

### After (5 files)
```
simple_simulator.py  # Core engine
algorithms.py        # Algorithms
scenarios.py         # Test data
runner.py            # Execution
visualizer.py        # Visualization
```

## Key Improvements

1. **Function Separation**: Clear separation between data, algorithms, execution, and visualization
2. **Reduced Redundancy**: Eliminated duplicate code across multiple files
3. **Easier Maintenance**: Single location for each functionality type
4. **Better Organization**: Logical grouping of related components
5. **Simpler Imports**: Cleaner import structure with centralized components

## File Sizes

| File | Lines | Purpose |
|------|-------|---------|
| `simple_simulator.py` | 332 | Core simulator classes |
| `algorithms.py` | 135 | All scheduling algorithms |
| `scenarios.py` | ~500 | All 24 test scenarios |
| `runner.py` | 250 | Experiment execution |
| `visualizer.py` | ~650 | All visualizations |

**Total**: ~1,867 lines (well-organized and maintainable)

## Testing

All consolidated files have been tested and verified:

```bash
✅ scenarios.py: 24 scenarios loaded
✅ algorithms.py: 7 algorithms loaded
✅ runner.py: ExperimentRunner class loaded successfully
✅ visualizer.py: SchedulingVisualizer class loaded successfully
```

## Next Steps

1. **Run complete experimental suite**: `python3 runner.py`
2. **Generate visualizations**: `python3 visualizer.py`
3. **Analyze results**: Review CSV and PNG outputs
4. **Write report**: Use visualizations in final report

## Documentation

Each file contains comprehensive docstrings:
- Module-level documentation explaining purpose
- Class docstrings with responsibilities
- Function docstrings with parameters and returns
- Inline comments for complex logic

## Maintainability

The consolidated structure makes future modifications easier:
- **Add new scenario**: Edit `scenarios.py`, add to appropriate category function
- **Add new algorithm**: Edit `algorithms.py`, add to `AVAILABLE_ALGORITHMS`
- **Add new visualization**: Edit `visualizer.py`, add new function
- **Modify metrics**: Edit `runner.py`, update `calculate_metrics()`

---

**Author**: PySchedule Development Team
**Date**: 2024
**License**: MIT
