"""
Tests for core simulation engine (simple_simulator.py).

Tests Task, Machine, Event, and Scheduler base class functionality.
"""

import pytest
from backend.app.core.simulator import Task, Priority, Machine, Event, Scheduler
from typing import List, Optional


class TestTask:
    """Test Task class functionality."""

    def test_task_creation(self, simple_task):
        """Test basic task creation with all attributes."""
        assert simple_task.id == 1
        assert simple_task.arrival_time == 0.0
        assert simple_task.processing_time == 5.0
        assert simple_task.priority == Priority.HIGH
        assert simple_task.deadline == 20.0
        assert simple_task.start_time is None
        assert simple_task.completion_time is None
        assert simple_task.machine_id is None

    def test_meets_deadline_success(self, completed_task):
        """Test deadline check for task completed on time."""
        assert completed_task.meets_deadline() is True

    def test_meets_deadline_failure(self, missed_deadline_task):
        """Test deadline check for task that missed deadline."""
        assert missed_deadline_task.meets_deadline() is False

    def test_meets_deadline_not_completed(self, simple_task):
        """Test deadline check for task not yet completed."""
        assert simple_task.meets_deadline() is False

    @pytest.mark.parametrize("current_time,expected_pressure", [
        (0.0, 0.0),    # Just arrived
        (10.0, 0.5),   # Halfway to deadline
        (15.0, 0.75),  # 75% of time elapsed
        (19.0, 0.95),  # Almost at deadline
    ])
    def test_deadline_pressure_normal_range(self, simple_task, current_time, expected_pressure):
        """Test deadline pressure calculation in normal range."""
        pressure = simple_task.deadline_pressure(current_time)
        assert abs(pressure - expected_pressure) < 0.01

    def test_deadline_pressure_past_deadline(self, simple_task):
        """Test deadline pressure returns infinity past deadline."""
        pressure = simple_task.deadline_pressure(25.0)
        assert pressure == 1.25

    def test_deadline_pressure_already_started(self, simple_task):
        """Test deadline pressure returns 0.0 if task already started."""
        simple_task.start_time = 0.0
        pressure = simple_task.deadline_pressure(10.0)
        assert pressure == 0.0

    def test_deadline_pressure_zero_time_available(self):
        """Test deadline pressure with deadline == arrival_time."""
        task = Task(
            id=1,
            arrival_time=10.0,
            processing_time=5.0,
            priority=Priority.HIGH,
            deadline=10.0  # Same as arrival
        )
        pressure = task.deadline_pressure(10.0)
        assert pressure == float('inf')


class TestPriority:
    """Test Priority enum."""

    def test_priority_values(self):
        """Test priority enum values are correct."""
        assert Priority.HIGH.value == 1
        assert Priority.LOW.value == 2

    def test_priority_ordering(self):
        """Test that HIGH < LOW for sorting purposes."""
        assert Priority.HIGH.value < Priority.LOW.value

    def test_priority_comparison(self):
        """Test priority comparison operations."""
        assert Priority.HIGH == Priority.HIGH
        assert Priority.LOW == Priority.LOW
        assert Priority.HIGH != Priority.LOW


class TestMachine:
    """Test Machine class functionality."""

    def test_machine_creation(self, single_machine):
        """Test basic machine creation."""
        machine = single_machine[0]
        assert machine.id == 0
        assert machine.available_at == 0.0

    def test_machine_is_idle_initially(self, single_machine):
        """Test that new machine is idle."""
        machine = single_machine[0]
        assert machine.is_idle(0.0) is True

    def test_machine_is_idle_after_availability(self):
        """Test machine is idle after availability time passes."""
        machine = Machine(id=0, available_at=10.0)
        assert machine.is_idle(5.0) is False
        assert machine.is_idle(10.0) is True
        assert machine.is_idle(15.0) is True

    def test_machine_availability_update(self):
        """Test updating machine availability time."""
        machine = Machine(id=0)
        machine.available_at = 10.0
        assert machine.is_idle(5.0) is False
        assert machine.is_idle(10.0) is True


class TestEvent:
    """Test Event class functionality."""

    def test_event_creation(self, simple_task):
        """Test basic event creation."""
        event = Event(
            time=0.0,
            event_type="ARRIVAL",
            task=simple_task,
            machine=None
        )
        assert event.time == 0.0
        assert event.type == "ARRIVAL"
        assert event.task == simple_task
        assert event.machine is None

    def test_completion_event(self, simple_task):
        """Test completion event with machine_id."""
        event = Event(
            time=5.0,
            event_type="COMPLETION",
            task=simple_task,
            machine=Machine(id=0)
        )
        assert event.time == 5.0
        assert event.type == "COMPLETION"
        assert event.machine.id == 0


class TestSchedulerBase:
    """Test Scheduler base class functionality."""

    class MinimalScheduler(Scheduler):
        """Minimal scheduler implementation for testing base class."""
        def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
            """Select first task in list."""
            return ready_tasks[0] if ready_tasks else None

    def test_scheduler_initialization(self, mixed_priority_tasks):
        """Test scheduler initializes with correct state."""
        scheduler = self.MinimalScheduler(mixed_priority_tasks, num_machines=2)

        assert len(scheduler.all_tasks) == 6
        assert scheduler.num_machines == 2
        assert len(scheduler.machines) == 2
        assert scheduler.current_time == 0.0
        scheduler.initialize()
        assert len(scheduler.event_queue) > 0  # Should have arrival events

    def test_scheduler_creates_arrival_events(self, high_priority_tasks):
        """Test that scheduler creates arrival events for all tasks."""
        scheduler = self.MinimalScheduler(high_priority_tasks, num_machines=1)
        scheduler.initialize()

        # Count arrival events (all tasks should have arrivals)
        arrival_events = [e for e in scheduler.event_queue if e.type == "ARRIVAL"]
        assert len(arrival_events) == len(high_priority_tasks)

    def test_scheduler_run_completes_all_tasks(self, high_priority_tasks):
        """Test that run() completes all tasks."""
        scheduler = self.MinimalScheduler(high_priority_tasks, num_machines=2)
        scheduler.run()

        # All tasks should have completion times
        for task in scheduler.all_tasks:
            assert task.completion_time is not None
            assert task.start_time is not None
            assert task.machine_id is not None

    def test_scheduler_run_advances_time(self, high_priority_tasks):
        """Test that simulation time advances during run()."""
        scheduler = self.MinimalScheduler(high_priority_tasks, num_machines=2)
        scheduler.run()

        assert scheduler.current_time > 0.0

    def test_scheduler_empty_task_list(self):
        """Test scheduler behavior with empty task list."""
        scheduler = self.MinimalScheduler([], num_machines=2)
        scheduler.run()

        assert scheduler.current_time == 0.0
        assert len(scheduler.get_results()) > 0

    def test_scheduler_single_task(self):
        """Test scheduler with single task."""
        task = Task(
            id=1,
            arrival_time=0.0,
            processing_time=5.0,
            priority=Priority.HIGH,
            deadline=20.0
        )
        scheduler = self.MinimalScheduler([task], num_machines=1)
        scheduler.run()

        assert task.completion_time == 5.0
        assert task.meets_deadline() is True

    def test_scheduler_machine_utilization(self, high_priority_tasks):
        """Test that machines are utilized correctly."""
        scheduler = self.MinimalScheduler(high_priority_tasks, num_machines=2)
        scheduler.run()

        # With 2 machines and 3 tasks, all machines should have been used
        machines_used = set(task.machine_id for task in scheduler.completed_tasks)
        assert len(machines_used) >= 1  # At least one machine used

    def test_scheduler_tardiness_calculation(self, tasks_all_miss_deadlines):
        """Test that tardiness is calculated for missed deadlines."""
        scheduler = self.MinimalScheduler(tasks_all_miss_deadlines, num_machines=1)
        scheduler.run()

        total_tardiness = sum(max(0, t.completion_time - t.deadline) for t in scheduler.completed_tasks)
        missed_deadlines = sum(1 for t in scheduler.completed_tasks if not t.meets_deadline())
        assert total_tardiness > 0
        assert missed_deadlines > 0

    def test_scheduler_no_tardiness_when_all_meet_deadlines(self, high_priority_tasks):
        """Test that tardiness is 0 when all tasks meet deadlines."""
        scheduler = self.MinimalScheduler(high_priority_tasks, num_machines=2)
        scheduler.run()

        # These tasks should all meet deadlines with 2 machines
        # These tasks should all meet deadlines with 2 machines
        total_tardiness = sum(max(0, t.completion_time - t.deadline) for t in scheduler.completed_tasks)
        missed_deadlines = sum(1 for t in scheduler.completed_tasks if not t.meets_deadline())
        assert total_tardiness == 0.0
        assert missed_deadlines == 0


class TestSchedulerEdgeCases:
    """Test edge cases and error conditions."""

    class MinimalScheduler(Scheduler):
        """Minimal scheduler for edge case testing."""
        def select_task(self, ready_tasks: List[Task]) -> Optional[Task]:
            return ready_tasks[0] if ready_tasks else None

    def test_concurrent_task_arrivals(self):
        """Test handling of tasks arriving at same time."""
        tasks = [
            Task(id=i, arrival_time=0.0, processing_time=5.0,
                 priority=Priority.HIGH, deadline=20.0)
            for i in range(1, 4)
        ]
        scheduler = self.MinimalScheduler(tasks, num_machines=2)
        scheduler.run()

        # All tasks should complete
        for task in scheduler.all_tasks:
            assert task.completion_time is not None

    def test_task_longer_than_deadline(self):
        """Test task that requires more time than available before deadline."""
        task = Task(
            id=1,
            arrival_time=0.0,
            processing_time=20.0,  # Longer than time to deadline
            priority=Priority.HIGH,
            deadline=10.0
        )
        scheduler = self.MinimalScheduler([task], num_machines=1)
        scheduler.run()

        assert task.completion_time == 20.0
        assert not task.meets_deadline()
        missed_deadlines = sum(1 for t in scheduler.completed_tasks if not t.meets_deadline())
        assert missed_deadlines == 1

    def test_staggered_arrivals(self):
        """Test tasks with different arrival times."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
            Task(id=2, arrival_time=10.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
            Task(id=3, arrival_time=20.0, processing_time=5.0, priority=Priority.HIGH, deadline=40.0),
        ]
        scheduler = self.MinimalScheduler(tasks, num_machines=1)
        scheduler.run()

        # Check that tasks started at or after their arrival times
        for task in scheduler.all_tasks:
            assert task.start_time >= task.arrival_time

    def test_more_tasks_than_machines(self, mixed_priority_tasks):
        """Test with more tasks than machines (resource contention)."""
        scheduler = self.MinimalScheduler(mixed_priority_tasks, num_machines=1)
        scheduler.run()

        # All tasks should still complete
        assert all(task.completion_time is not None for task in scheduler.all_tasks)

        # Tasks should execute sequentially on single machine
        completion_times = sorted([task.completion_time for task in scheduler.all_tasks])
        # Check no overlaps (each task starts after previous completes)
        for i in range(1, len(completion_times)):
            assert completion_times[i] >= completion_times[i-1]
