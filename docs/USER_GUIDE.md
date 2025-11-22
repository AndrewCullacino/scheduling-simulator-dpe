# Scheduling Simulator - User Guide

Welcome to the Scheduling Simulator User Guide. This document provides detailed instructions on how to configure simulations, interpret results, and understand the underlying algorithms.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Running a Simulation](#running-a-simulation)
3. [Algorithms Explained](#algorithms-explained)
4. [Understanding Results](#understanding-results)
5. [Troubleshooting](#troubleshooting)

## Getting Started

Access the simulator via the live demo: [https://scheduling-simulator-dpe.vercel.app/](https://scheduling-simulator-dpe.vercel.app/)

Or run locally:
```bash
./start.sh
```

## Running a Simulation

1.  **Select Algorithm**: Choose the scheduling algorithm you want to test from the dropdown menu.
2.  **Select Scenario**: Choose one of the 24 built-in scenarios.
    *   *Basic*: Simple tests to verify functionality.
    *   *Challenge*: Difficult cases that differentiate algorithms.
    *   *Extreme*: Stress tests designed to break specific algorithms.
    *   *Advanced*: Realistic workloads like Web Server or Database traffic.
3.  **Configure Machines**: Adjust the number of parallel machines (default is set by the scenario).
4.  **Run**: Click the "Run Simulation" button.

## Algorithms Explained

### SPT (Shortest Processing Time)
*   **Strategy**: Always selects the task with the shortest processing time.
*   **Pros**: Minimizes average waiting time.
*   **Cons**: Ignores deadlines and priorities. Can starve long tasks.

### EDF (Earliest Deadline First)
*   **Strategy**: Selects the task with the closest deadline.
*   **Pros**: Optimal for single-machine scheduling (if feasible).
*   **Cons**: Can perform poorly in overload conditions (domino effect).

### Priority-First
*   **Strategy**: Strictly schedules HIGH priority tasks before LOW priority tasks.
*   **Pros**: Guarantees service for important tasks.
*   **Cons**: Can cause starvation of low-priority tasks.

### DPE (Dynamic Priority Elevation)
*   **Strategy**: A hybrid approach. Starts as Priority-First, but "elevates" low-priority tasks to HIGH if they are in danger of missing their deadline.
*   **Alpha Parameter**: Controls the sensitivity.
    *   `α = 0.3`: Aggressive elevation (helps low priority early).
    *   `α = 0.7`: Conservative elevation (only helps when very urgent).

## Understanding Results

### Gantt Chart
The visual timeline shows:
*   **Red Blocks**: High Priority Tasks.
*   **Blue Blocks**: Low Priority Tasks.
*   **X-Axis**: Time units.
*   **Y-Axis**: Machine ID.

### Metrics
*   **Makespan**: The total time to complete all tasks.
*   **Success Rate**: Percentage of tasks that met their deadline.
*   **Logs**: Detailed event log showing Arrival, Start, and Completion times.

## Troubleshooting

### "Failed to run simulation"
*   **Cause**: The frontend cannot connect to the backend.
*   **Fix**:
    *   If running locally, ensure the backend is running on port 8000.
    *   If on the web, the free backend instance on Render might be "sleeping". Wait 30-60 seconds and try again.

### "No idle machines"
*   **Cause**: All machines are busy.
*   **Fix**: This is normal behavior. Tasks will wait in the queue until a machine becomes free.
