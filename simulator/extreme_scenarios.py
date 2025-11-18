"""
Extreme Test Scenarios for COMP3821 Scheduling Project
=======================================================

Extreme test scenarios designed to maximize algorithm differentiation.
These scenarios create stress conditions to reveal algorithm limits and trade-offs.

Author: Group 5
Date: November 2024
"""

from simple_simulator import Task, Priority


def get_extreme_scenarios():
    """
    Define extreme test scenarios designed to maximize differences.

    These scenarios are designed to:
    - Guarantee starvation for Priority-First
    - Test alpha parameter sensitivity at extreme values
    - Force SPT to fail spectacularly
    - Test multiple starvation scenarios
    - Create feasible scenarios that only some algorithms can solve

    Returns:
        list: List of scenario dictionaries, each containing:
            - name (str): Scenario name
            - description (str): What the scenario tests
            - tasks (list): List of Task objects
            - num_machines (int): Number of parallel machines
    """

    scenarios = []

    # Extreme 1: Guaranteed starvation for Priority-First
    scenarios.append({
        'name': 'Extreme 1: Starvation Guaranteed',
        'description': 'Priority-First WILL starve low-priority',
        'tasks': [
            Task(1, 0, 5, Priority.LOW, 16),
            Task(2, 0, 2, Priority.HIGH, 20),
            Task(3, 2, 2, Priority.HIGH, 22),
            Task(4, 4, 2, Priority.HIGH, 24),
            Task(5, 6, 2, Priority.HIGH, 26),
            Task(6, 8, 2, Priority.HIGH, 28),
            Task(7, 10, 2, Priority.HIGH, 30),
        ],
        'num_machines': 1
    })

    # Extreme 2: Alpha value critical
    scenarios.append({
        'name': 'Extreme 2: Alpha Critical',
        'description': 'α=0.5 succeeds, α=0.9 fails',
        'tasks': [
            Task(1, 0, 6, Priority.LOW, 25),
            Task(2, 0, 3, Priority.HIGH, 30),
            Task(3, 3, 3, Priority.HIGH, 33),
            Task(4, 6, 3, Priority.HIGH, 36),
            Task(5, 9, 3, Priority.HIGH, 39),
            Task(6, 12, 3, Priority.HIGH, 42),
            Task(7, 15, 3, Priority.HIGH, 45),
            Task(8, 18, 3, Priority.HIGH, 48),
        ],
        'num_machines': 1
    })

    # Extreme 3: SPT clearly fails
    scenarios.append({
        'name': 'Extreme 3: SPT Fails',
        'description': 'SPT ignores deadlines entirely',
        'tasks': [
            Task(1, 0, 1, Priority.HIGH, 50),
            Task(2, 0, 10, Priority.HIGH, 11),
            Task(3, 0, 2, Priority.HIGH, 45),
            Task(4, 0, 5, Priority.HIGH, 7),
        ],
        'num_machines': 2
    })

    # Extreme 4: Multiple starvation
    scenarios.append({
        'name': 'Extreme 4: Multiple Starvation',
        'description': 'Multiple low-priority at risk',
        'tasks': [
            Task(1, 0, 4, Priority.LOW, 14),
            Task(2, 1, 4, Priority.LOW, 16),
            Task(3, 2, 4, Priority.LOW, 18),
            Task(4, 0, 2, Priority.HIGH, 25),
            Task(5, 2, 2, Priority.HIGH, 27),
            Task(6, 4, 2, Priority.HIGH, 29),
            Task(7, 6, 2, Priority.HIGH, 31),
            Task(8, 8, 2, Priority.HIGH, 33),
            Task(9, 10, 2, Priority.HIGH, 35),
        ],
        'num_machines': 2
    })

    # Extreme 5: Only EDF and DPE can solve
    scenarios.append({
        'name': 'Extreme 5: Priority-First Impossible',
        'description': 'Feasible but not for Priority-First',
        'tasks': [
            Task(1, 0, 5, Priority.LOW, 6),    # MUST go first!
            Task(2, 0, 3, Priority.HIGH, 15),
            Task(3, 0, 2, Priority.HIGH, 20),
        ],
        'num_machines': 1
    })

    return scenarios
