"""
Simple Test Scenarios for COMP3821 Scheduling Project
======================================================

Basic test scenarios for validating algorithm implementations.
These scenarios test fundamental scheduling behaviors under normal conditions.

Author: Group 5
Date: November 2024
"""

from simple_simulator import Task, Priority


def get_simple_scenarios():
    """
    Define basic test scenarios for algorithm validation.

    Returns:
        list: List of scenario dictionaries, each containing:
            - name (str): Scenario name
            - description (str): What the scenario tests
            - tasks (list): List of Task objects
            - num_machines (int): Number of parallel machines
    """

    scenarios = []

    # Scenario 1: Light Load (Easy baseline)
    scenarios.append({
        'name': 'Light Load',
        'description': 'Few tasks, should all meet deadlines',
        'tasks': [
            Task(1, 0, 3, Priority.HIGH, 10),
            Task(2, 0, 2, Priority.HIGH, 12),
            Task(3, 1, 4, Priority.HIGH, 15),
            Task(4, 0, 5, Priority.LOW, 25),
            Task(5, 2, 6, Priority.LOW, 30),
        ],
        'num_machines': 2
    })

    # Scenario 2: Heavy Load
    scenarios.append({
        'name': 'Heavy Load',
        'description': 'Many tasks, tight deadlines',
        'tasks': [
            Task(1, 0, 4, Priority.HIGH, 9),
            Task(2, 1, 3, Priority.HIGH, 10),
            Task(3, 2, 3, Priority.HIGH, 12),
            Task(4, 0, 5, Priority.HIGH, 14),
            Task(5, 0, 7, Priority.LOW, 20),
            Task(6, 1, 6, Priority.LOW, 22),
            Task(7, 2, 5, Priority.LOW, 25),
        ],
        'num_machines': 3
    })

    # Scenario 3: Starvation Test
    scenarios.append({
        'name': 'Starvation Test',
        'description': 'Continuous high priority, will low priority starve?',
        'tasks': [
            Task(1, 0, 2, Priority.HIGH, 8),
            Task(2, 1, 2, Priority.HIGH, 10),
            Task(3, 2, 2, Priority.HIGH, 12),
            Task(4, 3, 2, Priority.HIGH, 14),
            Task(5, 4, 2, Priority.HIGH, 16),
            Task(6, 0, 4, Priority.LOW, 15),  # Will this get starved?
            Task(7, 1, 4, Priority.LOW, 18),  # And this?
        ],
        'num_machines': 2
    })

    # Scenario 4: Batch Arrival (all tasks arrive simultaneously)
    scenarios.append({
        'name': 'Batch Arrival',
        'description': 'All tasks arrive at once',
        'tasks': [
            Task(1, 0, 3, Priority.HIGH, 8),
            Task(2, 0, 4, Priority.HIGH, 10),
            Task(3, 0, 2, Priority.HIGH, 12),
            Task(4, 0, 5, Priority.LOW, 20),
            Task(5, 0, 6, Priority.LOW, 25),
            Task(6, 0, 3, Priority.LOW, 22),
        ],
        'num_machines': 2
    })

    return scenarios
