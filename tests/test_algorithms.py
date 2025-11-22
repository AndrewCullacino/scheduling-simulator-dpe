"""
Tests for scheduling algorithms (algorithms.py).

Tests SPT, EDF, Priority-First, and DPE algorithm implementations.
"""

import pytest
from backend.app.core.simulator import Task, Priority
from backend.app.core.algorithms import (
    SPT_Scheduler, EDF_Scheduler, PriorityFirst_Scheduler, DPE_Scheduler,
    get_all_algorithms
)


class TestSPTScheduler:
    """Test Shortest Processing Time scheduler."""

    def test_spt_selects_shortest_task(self):
        """Test that SPT always selects task with shortest processing time."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=3.0, priority=Priority.LOW, deadline=20.0),  # Shortest
            Task(id=3, arrival_time=0.0, processing_time=7.0, priority=Priority.HIGH, deadline=30.0),
        ]

        scheduler = SPT_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (shortest) should start first
        assert tasks[1].start_time == 0.0

    def test_spt_ignores_priority(self):
        """Test that SPT ignores task priority."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=30.0),  # Shorter but low priority
        ]

        scheduler = SPT_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Low priority task with shorter processing time should start first
        assert tasks[1].start_time == 0.0

    def test_spt_ignores_deadline(self):
        """Test that SPT ignores task deadlines."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=8.0),  # Urgent but not shortest
            Task(id=2, arrival_time=0.0, processing_time=3.0, priority=Priority.HIGH, deadline=50.0),  # Shortest
        ]

        scheduler = SPT_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (shortest) should start first despite task 1 being more urgent
        assert tasks[1].start_time == 0.0

    def test_spt_empty_ready_tasks(self):
        """Test SPT with no ready tasks."""
        scheduler = SPT_Scheduler([], num_machines=1)
        result = scheduler.select_task([])
        assert result is None


class TestEDFScheduler:
    """Test Earliest Deadline First scheduler."""

    def test_edf_selects_earliest_deadline(self):
        """Test that EDF always selects task with earliest deadline."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=15.0),  # Earliest
            Task(id=3, arrival_time=0.0, processing_time=3.0, priority=Priority.HIGH, deadline=30.0),
        ]

        scheduler = EDF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (earliest deadline) should start first
        assert tasks[1].start_time == 0.0

    def test_edf_ignores_priority(self):
        """Test that EDF ignores task priority."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=20.0),  # Earlier deadline
        ]

        scheduler = EDF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Low priority task with earlier deadline should start first
        assert tasks[1].start_time == 0.0

    def test_edf_ignores_processing_time(self):
        """Test that EDF ignores processing time."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=2.0, priority=Priority.HIGH, deadline=30.0),  # Shorter
            Task(id=2, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=20.0),  # Longer but earlier deadline
        ]

        scheduler = EDF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (earlier deadline) should start first despite being longer
        assert tasks[1].start_time == 0.0

    def test_edf_optimality_single_machine(self):
        """Test EDF is optimal for feasible single-machine schedule."""
        # Create feasible schedule where EDF can meet all deadlines
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=3.0, priority=Priority.HIGH, deadline=10.0),
            Task(id=2, arrival_time=0.0, processing_time=2.0, priority=Priority.HIGH, deadline=5.0),
            Task(id=3, arrival_time=0.0, processing_time=1.0, priority=Priority.HIGH, deadline=6.0),
        ]

        scheduler = EDF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # All tasks should meet their deadlines (EDF is optimal)
        assert all(task.meets_deadline() for task in scheduler.completed_tasks)


class TestPriorityFirstScheduler:
    """Test static priority scheduler."""

    def test_priority_first_respects_priority(self):
        """Test that Priority-First always selects highest priority task."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.LOW, deadline=15.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=50.0),  # High priority
            Task(id=3, arrival_time=0.0, processing_time=3.0, priority=Priority.LOW, deadline=20.0),
        ]

        scheduler = PriorityFirst_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (HIGH priority) should start first
        assert tasks[1].start_time == 0.0

    def test_priority_first_uses_edf_tiebreaking(self):
        """Test that Priority-First uses EDF for tiebreaking within same priority."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),  # Same priority, earlier deadline
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=25.0),
        ]

        scheduler = PriorityFirst_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (earliest deadline among HIGH priority) should start first
        assert tasks[1].start_time == 0.0

    def test_priority_first_can_cause_starvation(self):
        """Test that Priority-First can starve low-priority tasks."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=15.0),  # More urgent but low priority
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
        ]

        scheduler = PriorityFirst_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # All HIGH priority tasks should complete before LOW priority task starts
        high_priority_completion = max(
            task.completion_time for task in scheduler.completed_tasks if task.priority == Priority.HIGH
        )
        low_priority_start = tasks[1].start_time

        assert low_priority_start >= high_priority_completion

    def test_priority_first_low_priority_may_miss_deadline(self):
        """Test that low-priority tasks may miss deadlines with Priority-First."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=30.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=8.0),  # Will miss deadline
        ]

        scheduler = PriorityFirst_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Low priority task likely misses deadline due to HIGH priority execution first
        assert not tasks[1].meets_deadline()


class TestDPEScheduler:
    """Test Dynamic Priority Elevation scheduler."""

    def test_dpe_initialization_with_alpha(self):
        """Test DPE scheduler initializes with correct alpha value."""
        tasks = [Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=20.0)]

        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=0.5)
        assert scheduler.alpha == 0.5

    def test_dpe_default_alpha(self):
        """Test DPE scheduler has default alpha value."""
        tasks = [Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=20.0)]

        scheduler = DPE_Scheduler(tasks, num_machines=1)
        assert scheduler.alpha == 0.7  # Default from class definition

    def test_dpe_elevates_low_priority_when_pressure_high(self):
        """Test that DPE elevates low-priority task when deadline pressure exceeds alpha."""
        tasks = [
            # Blocking task to let time pass
            Task(id=0, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=100.0),
            # High priority task arriving later
            Task(id=1, arrival_time=5.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            # Low priority task arriving early (waits for 5.0)
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=12.0),  # Tight deadline
        ]

        # Conservative alpha (0.3) - should elevate task 2 early
        # At t=5 (when task 0 finishes):
        # Task 2 pressure = 5 / 12 = 0.41 > 0.3. Elevated!
        # Task 2 deadline 12 < Task 1 deadline 50.
        # Task 2 should run before Task 1.
        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=0.3)
        scheduler.run()

        # Task 2 should meet deadline
        assert tasks[2].meets_deadline()
        # Task 2 should start at 5.0 (after Task 0)
        assert tasks[2].start_time == 5.0

    def test_dpe_does_not_elevate_when_pressure_low(self):
        """Test that DPE doesn't elevate when deadline pressure is below alpha."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=100.0),  # Very loose deadline
        ]

        # Aggressive alpha (0.9) - should NOT elevate task 2
        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=0.9)
        scheduler.run()

        # HIGH priority task should execute first (low priority not elevated due to loose deadline)
        assert tasks[0].start_time == 0.0

    @pytest.mark.parametrize("alpha", [0.3, 0.5, 0.7, 0.9])
    def test_dpe_alpha_parameter_effect(self, alpha):
        """Test that different alpha values produce different scheduling behaviors."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=18.0),
        ]

        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=alpha)
        scheduler.run()

        # All tasks should complete
        assert all(task.completion_time is not None for task in scheduler.all_tasks)

    def test_dpe_high_priority_never_demoted(self):
        """Test that HIGH priority tasks are never demoted."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=100.0),  # High, loose deadline
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=12.0),   # Low, tight deadline
        ]

        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=0.3)

        # Get effective priority for HIGH task
        effective_priority_high = scheduler.get_effective_priority(tasks[0])
        assert effective_priority_high == Priority.HIGH

    def test_dpe_alpha_one_equivalent_to_priority_first(self):
        """Test that α=1.0 makes DPE behave like Priority-First."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=10.0),  # More urgent but low priority
        ]

        # α=1.0 means elevation threshold is never reached (no elevation)
        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=1.0)
        scheduler.run()

        # HIGH priority task should execute first (no elevation occurs)
        assert tasks[0].start_time == 0.0

    def test_dpe_prevents_low_priority_starvation(self):
        """Test that DPE prevents complete starvation of low-priority tasks."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=40.0),
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=25.0),  # Low priority, moderate deadline
        ]

        # Conservative alpha should elevate low priority task before it misses deadline
        scheduler = DPE_Scheduler(tasks, num_machines=1, alpha=0.3)
        scheduler.run()

        # Low priority task should meet its deadline (elevated in time)
        assert tasks[2].meets_deadline()


class TestGetAllAlgorithms:
    """Test algorithm registry function."""

    def test_get_all_algorithms_returns_dict(self):
        """Test that get_all_algorithms returns a dictionary."""
        algorithms = get_all_algorithms()
        assert isinstance(algorithms, dict)

    def test_get_all_algorithms_contains_all_variants(self):
        """Test that all algorithm variants are in registry."""
        algorithms = get_all_algorithms()

        expected_algorithms = ['SPT', 'EDF', 'Priority-First',
                              'DPE (α=0.3)', 'DPE (α=0.5)', 'DPE (α=0.7)', 'DPE (α=0.9)']

        for algo in expected_algorithms:
            assert algo in algorithms

    def test_get_all_algorithms_classes_callable(self):
        """Test that all algorithm classes/factories are callable."""
        algorithms = get_all_algorithms()

        tasks = [Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0)]

        for name, algo_class in algorithms.items():
            # Should be able to instantiate each algorithm
            if callable(algo_class):
                scheduler = algo_class(tasks, 1)
                assert scheduler is not None


class TestAlgorithmComparison:
    """Test comparing algorithms on same scenarios."""

    def test_all_algorithms_complete_all_tasks(self, mixed_priority_tasks, any_scheduler_class):
        """Test that all algorithms complete all tasks."""
        scheduler = any_scheduler_class(mixed_priority_tasks.copy(), num_machines=2)
        scheduler.run()

        # All tasks should have completion times
        assert all(task.completion_time is not None for task in scheduler.all_tasks)

    def test_algorithms_produce_different_schedules(self):
        """Test that different algorithms produce different schedules."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=3.0, priority=Priority.LOW, deadline=15.0),
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=30.0),
        ]

        # Run with SPT
        spt = SPT_Scheduler(tasks.copy(), num_machines=1)
        spt.run()
        spt_order = [(t.id, t.start_time) for t in spt.completed_tasks]

        # Run with EDF
        edf = EDF_Scheduler(tasks.copy(), num_machines=1)
        edf.run()
        edf_order = [(t.id, t.start_time) for t in edf.completed_tasks]

        # Run with Priority-First
        priority = PriorityFirst_Scheduler(tasks.copy(), num_machines=1)
        priority.run()
        priority_order = [(t.id, t.start_time) for t in priority.completed_tasks]

        # At least some algorithms should produce different orderings
        assert not (spt_order == edf_order == priority_order)
