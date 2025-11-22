"""
Tests for new scheduling algorithms (FCFS, HRRN, MLF).
"""

import pytest
from backend.app.core.simulator import Task, Priority
from backend.app.core.algorithms import (
    FCFS_Scheduler, HRRN_Scheduler, MLF_Scheduler
)


class TestFCFSScheduler:
    """Test First Come First Served scheduler."""

    def test_fcfs_selects_by_arrival_time(self):
        """Test that FCFS selects tasks based on arrival time."""
        tasks = [
            Task(id=1, arrival_time=10.0, processing_time=5.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=2, arrival_time=5.0, processing_time=5.0, priority=Priority.LOW, deadline=50.0),
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=50.0),
        ]

        scheduler = FCFS_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Order should be Task 3 (arrival 0), Task 2 (arrival 5), Task 1 (arrival 10)
        assert tasks[2].start_time == 0.0  # Task 3
        assert tasks[1].start_time == 5.0  # Task 2
        assert tasks[0].start_time == 10.0 # Task 1

    def test_fcfs_tie_break_by_id(self):
        """Test that FCFS uses ID as tie-breaker for same arrival time."""
        tasks = [
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=50.0),
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=50.0),
        ]

        scheduler = FCFS_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 1 should start first due to lower ID
        assert tasks[1].start_time == 0.0


class TestHRRNScheduler:
    """Test Highest Response Ratio Next scheduler."""

    def test_hrrn_prefers_long_waiting_tasks(self):
        """Test that HRRN prefers tasks that have waited longer."""
        # Current time will be 10.0 after first task finishes
        # Task 1: arrives 0, proc 10. finishes at 10.
        # Task 2: arrives 0, proc 2. wait=10. RR = (10+2)/2 = 6.
        # Task 3: arrives 9, proc 1. wait=1. RR = (1+1)/1 = 2.
        
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=100.0),
            Task(id=2, arrival_time=0.0, processing_time=2.0, priority=Priority.LOW, deadline=100.0),
            Task(id=3, arrival_time=9.0, processing_time=1.0, priority=Priority.HIGH, deadline=100.0),
        ]

        scheduler = HRRN_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 1 runs first (0-10)
        assert tasks[0].start_time == 0.0
        
        # At t=10:
        # Task 2: wait=10, service=2, RR=6
        # Task 3: wait=1, service=1, RR=2
        # Task 2 should run next despite being longer
        assert tasks[1].start_time == 10.0
        assert tasks[2].start_time == 12.0

    def test_hrrn_prefers_short_tasks_when_wait_equal(self):
        """Test that HRRN prefers shorter tasks when waiting times are similar."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=Priority.HIGH, deadline=100.0), # Runs first
            Task(id=2, arrival_time=0.0, processing_time=2.0, priority=Priority.LOW, deadline=100.0),
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=100.0),
        ]

        scheduler = HRRN_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # At t=10:
        # Task 2: wait=10, service=2, RR=6
        # Task 3: wait=10, service=5, RR=3
        # Task 2 should run next
        assert tasks[1].start_time == 10.0


class TestMLFScheduler:
    """Test Minimum Laxity First scheduler."""

    def test_mlf_selects_least_laxity(self):
        """Test that MLF selects task with least laxity."""
        # Laxity = (Deadline - CurrentTime) - ProcessingTime
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=10.0), # Laxity = 10 - 5 = 5
            Task(id=2, arrival_time=0.0, processing_time=5.0, priority=Priority.LOW, deadline=6.0),   # Laxity = 6 - 5 = 1 (Urgent!)
            Task(id=3, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0), # Laxity = 20 - 5 = 15
        ]

        scheduler = MLF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 has least laxity, should run first
        assert tasks[1].start_time == 0.0

    def test_mlf_dynamic_laxity(self):
        """Test that laxity is calculated dynamically based on current time."""
        # Task 1: arrives 0, proc 5, deadline 20.
        # Task 2: arrives 4, proc 2, deadline 8.
        
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=5.0, priority=Priority.HIGH, deadline=20.0),
            Task(id=2, arrival_time=4.0, processing_time=2.0, priority=Priority.LOW, deadline=8.0),
        ]

        scheduler = MLF_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 1 starts at 0 (only one available)
        assert tasks[0].start_time == 0.0
        
        # Task 1 finishes at 5.
        # At t=5:
        # Task 2 is available.
        # Task 2 starts at 5.
        assert tasks[1].start_time == 5.0
