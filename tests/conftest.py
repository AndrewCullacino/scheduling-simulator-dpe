"""
Pytest fixtures for PySchedule test suite.

Provides reusable test data and configured objects for all test modules.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from simple_simulator import Task, Priority, Machine, Scheduler
from algorithms import SPT_Scheduler, EDF_Scheduler, PriorityFirst_Scheduler, DPE_Scheduler


# =============================================================================
# Task Fixtures
# =============================================================================

@pytest.fixture
def simple_task():
    """Single task with reasonable parameters."""
    return Task(
        id=1,
        arrival_time=0.0,
        processing_time=5.0,
        priority=Priority.HIGH,
        deadline=20.0
    )


@pytest.fixture
def high_priority_tasks():
    """List of high-priority tasks."""
    return [
        Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
        Task(id=2, arrival_time=2.0, processing_time=3.0, priority=Priority.HIGH, deadline=15.0),
        Task(id=3, arrival_time=5.0, processing_time=4.0, priority=Priority.HIGH, deadline=25.0),
    ]


@pytest.fixture
def low_priority_tasks():
    """List of low-priority tasks."""
    return [
        Task(id=4, arrival_time=0.0, processing_time=6.0, priority=Priority.LOW, deadline=30.0),
        Task(id=5, arrival_time=3.0, processing_time=4.0, priority=Priority.LOW, deadline=25.0),
        Task(id=6, arrival_time=6.0, processing_time=5.0, priority=Priority.LOW, deadline=35.0),
    ]


@pytest.fixture
def mixed_priority_tasks(high_priority_tasks, low_priority_tasks):
    """Combined list of high and low priority tasks."""
    return high_priority_tasks + low_priority_tasks


@pytest.fixture
def tasks_with_tight_deadlines():
    """Tasks with deadlines that are difficult to meet."""
    return [
        Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=12.0),
        Task(id=2, arrival_time=0.0, processing_time=8.0, priority=Priority.LOW, deadline=10.0),
        Task(id=3, arrival_time=5.0, processing_time=6.0, priority=Priority.HIGH, deadline=12.0),
    ]


@pytest.fixture
def tasks_all_miss_deadlines():
    """Tasks that are impossible to complete on time (for testing failure cases)."""
    return [
        Task(id=1, arrival_time=0.0, processing_time=20.0, priority=Priority.HIGH, deadline=5.0),
        Task(id=2, arrival_time=0.0, processing_time=15.0, priority=Priority.LOW, deadline=3.0),
    ]


# =============================================================================
# Machine Fixtures
# =============================================================================

@pytest.fixture
def single_machine():
    """Single machine configuration."""
    return [Machine(id=0)]


@pytest.fixture
def two_machines():
    """Two machine configuration."""
    return [Machine(id=0), Machine(id=1)]


@pytest.fixture
def four_machines():
    """Four machine configuration."""
    return [Machine(id=i) for i in range(4)]


# =============================================================================
# Scenario Fixtures
# =============================================================================

@pytest.fixture
def simple_scenario():
    """Simple test scenario with predictable behavior."""
    return {
        "name": "Test Scenario - Simple",
        "description": "Simple test case for validation",
        "tasks": [
            {"id": 1, "arrival_time": 0.0, "processing_time": 5.0, "priority": "HIGH", "deadline": 20.0},
            {"id": 2, "arrival_time": 0.0, "processing_time": 3.0, "priority": "LOW", "deadline": 15.0},
            {"id": 3, "arrival_time": 5.0, "processing_time": 4.0, "priority": "HIGH", "deadline": 25.0},
        ],
        "num_machines": 2
    }


@pytest.fixture
def complex_scenario():
    """Complex scenario with multiple machines and mixed priorities."""
    return {
        "name": "Test Scenario - Complex",
        "description": "Complex test case with resource contention",
        "tasks": [
            {"id": i, "arrival_time": float(i % 3), "processing_time": float(3 + i % 4),
             "priority": "HIGH" if i % 2 == 0 else "LOW", "deadline": float(20 + i * 5)}
            for i in range(1, 11)
        ],
        "num_machines": 3
    }


# =============================================================================
# Scheduler Fixtures
# =============================================================================

@pytest.fixture
def spt_scheduler(mixed_priority_tasks):
    """SPT scheduler with mixed priority tasks."""
    return SPT_Scheduler(mixed_priority_tasks.copy(), num_machines=2)


@pytest.fixture
def edf_scheduler(mixed_priority_tasks):
    """EDF scheduler with mixed priority tasks."""
    return EDF_Scheduler(mixed_priority_tasks.copy(), num_machines=2)


@pytest.fixture
def priority_first_scheduler(mixed_priority_tasks):
    """Priority-First scheduler with mixed priority tasks."""
    return PriorityFirst_Scheduler(mixed_priority_tasks.copy(), num_machines=2)


@pytest.fixture
def dpe_scheduler_conservative(mixed_priority_tasks):
    """DPE scheduler with conservative α=0.3."""
    return DPE_Scheduler(mixed_priority_tasks.copy(), num_machines=2, alpha=0.3)


@pytest.fixture
def dpe_scheduler_aggressive(mixed_priority_tasks):
    """DPE scheduler with aggressive α=0.9."""
    return DPE_Scheduler(mixed_priority_tasks.copy(), num_machines=2, alpha=0.9)


# =============================================================================
# Helper Fixtures
# =============================================================================

@pytest.fixture
def completed_task():
    """Task with completion information filled in."""
    task = Task(
        id=1,
        arrival_time=0.0,
        processing_time=5.0,
        priority=Priority.HIGH,
        deadline=20.0
    )
    task.start_time = 0.0
    task.completion_time = 5.0
    task.machine_id = 0
    return task


@pytest.fixture
def missed_deadline_task():
    """Task that missed its deadline."""
    task = Task(
        id=2,
        arrival_time=0.0,
        processing_time=10.0,
        priority=Priority.LOW,
        deadline=5.0
    )
    task.start_time = 0.0
    task.completion_time = 10.0
    task.machine_id = 0
    return task


# =============================================================================
# Parametrize Fixtures (for testing multiple algorithms)
# =============================================================================

@pytest.fixture(params=[
    SPT_Scheduler,
    EDF_Scheduler,
    PriorityFirst_Scheduler,
    lambda tasks, num_machines: DPE_Scheduler(tasks, num_machines, alpha=0.5)
])
def any_scheduler_class(request):
    """Parametrized fixture that provides each scheduler class in turn."""
    return request.param


@pytest.fixture(params=[0.3, 0.5, 0.7, 0.9])
def dpe_alpha_values(request):
    """Parametrized fixture for testing different DPE alpha values."""
    return request.param
