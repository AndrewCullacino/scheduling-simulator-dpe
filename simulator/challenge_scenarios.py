"""
Challenge Test Scenarios for COMP3821 Scheduling Project
=========================================================

Challenging test scenarios designed to reveal algorithm differences.
These scenarios expose weaknesses and strengths of different scheduling approaches.

Author: Group 5
Date: November 2024
"""

from simple_simulator import Task, Priority


def get_challenge_scenarios():
    """
    Define challenging test scenarios that reveal algorithm differences.

    These scenarios are designed to:
    - Show when SPT fails due to deadline blindness
    - Demonstrate starvation risks in Priority-First
    - Test infeasible scenarios
    - Reveal DPE alpha parameter sensitivity
    - Expose priority inversion problems

    Returns:
        list: List of scenario dictionaries, each containing:
            - name (str): Scenario name
            - description (str): What the scenario tests
            - tasks (list): List of Task objects
            - num_machines (int): Number of parallel machines
    """

    scenarios = []

    # Challenge 1: SPT ignores tight deadlines
    scenarios.append({
        'name': 'Challenge 1: SPT vs EDF',
        'description': 'SPT schedules short tasks, missing tight deadlines',
        'tasks': [
            Task(1, 0, 2, Priority.HIGH, 30),
            Task(2, 0, 5, Priority.HIGH, 6),   # TIGHT deadline
            Task(3, 0, 1, Priority.HIGH, 25),
            Task(4, 0, 4, Priority.HIGH, 5),   # TIGHT deadline
        ],
        'num_machines': 2
    })

    # Challenge 2: Starvation test
    scenarios.append({
        'name': 'Challenge 2: Starvation',
        'description': 'Continuous high-priority tasks starve low-priority',
        'tasks': [
            Task(1, 0, 3, Priority.LOW, 8),    # Will starve?
            Task(2, 0, 2, Priority.HIGH, 15),
            Task(3, 1, 2, Priority.HIGH, 16),
            Task(4, 2, 2, Priority.HIGH, 17),
            Task(5, 3, 2, Priority.HIGH, 18),
            Task(6, 1, 3, Priority.LOW, 10),   # Will starve?
        ],
        'num_machines': 2
    })

    # Challenge 3: Infeasible (all should fail)
    scenarios.append({
        'name': 'Challenge 3: Impossible',
        'description': 'Mathematically impossible deadlines',
        'tasks': [
            Task(1, 0, 5, Priority.HIGH, 5),
            Task(2, 0, 5, Priority.HIGH, 5),
            Task(3, 0, 5, Priority.HIGH, 5),
            Task(4, 0, 5, Priority.HIGH, 5),
        ],
        'num_machines': 2
    })

    # Challenge 4: DPE Alpha sensitivity
    scenarios.append({
        'name': 'Challenge 4: Alpha Matters',
        'description': 'Different α values produce different results',
        'tasks': [
            Task(1, 0, 4, Priority.LOW, 12),
            Task(2, 0, 2, Priority.HIGH, 20),
            Task(3, 1, 2, Priority.HIGH, 22),
            Task(4, 2, 2, Priority.HIGH, 24),
            Task(5, 1, 3, Priority.LOW, 15),
        ],
        'num_machines': 2
    })

    # Challenge 5: Priority inversion
    scenarios.append({
        'name': 'Challenge 5: Priority Inversion',
        'description': 'Low-priority blocks high-priority on single machine',
        'tasks': [
            Task(1, 0, 8, Priority.LOW, 30),
            Task(2, 2, 3, Priority.HIGH, 6),   # Arrives late but urgent!
            Task(3, 3, 2, Priority.HIGH, 8),
        ],
        'num_machines': 1
    })

    return scenarios
