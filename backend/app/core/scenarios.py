"""
Test Scenarios for Real-Time Scheduling Research
=================================================

All test scenarios consolidated in one file for easier management.
Contains 24 scenarios across 5 categories:
- Simple (4 scenarios): Basic validation scenarios
- Challenge (5 scenarios): Algorithm differentiation tests
- Extreme (5 scenarios): Stress tests and edge cases
- Advanced (5 scenarios): Realistic multi-machine workloads
- New (5 scenarios): Alpha sensitivity and specialized tests

Author: PySchedule Development Team
Date: 2024
"""

from typing import Dict, List, Any
from .simulator import Task, Priority


def get_all_scenarios() -> List[Dict[str, Any]]:
    """
    Get all 24 test scenarios.

    Returns:
        List of scenario dictionaries, each containing:
            - name (str): Scenario name
            - description (str): What the scenario tests
            - tasks (List[Task]): List of Task objects
            - num_machines (int): Number of parallel machines
    """
    return (
        get_simple_scenarios() +
        get_challenge_scenarios() +
        get_extreme_scenarios() +
        get_advanced_scenarios() +
        get_new_experiments()
    )


def get_simple_scenarios() -> List[Dict[str, Any]]:
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


def get_challenge_scenarios() -> List[Dict[str, Any]]:
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


"""
Extreme Test Scenarios for Scheduling Research
==============================================

Extreme test scenarios designed to maximize algorithm differentiation.
These scenarios create stress conditions to reveal algorithm limits and trade-offs.

Author: PySchedule Development Team
Date: 2024
"""



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


"""
Advanced Test Scenarios for Scheduling Research
================================================

Advanced scenarios designed to fill gaps in current test coverage:
- Multi-machine utilization and load balancing
- Realistic workload patterns (web server, database)
- Burst arrival patterns and dynamic adaptation
- Machine saturation and oversubscription handling

These scenarios complement existing basic, challenge, and extreme scenarios
by testing parallel efficiency and real-world applicability.

Author: PySchedule Development Team
Date: 2024
"""



def get_advanced_scenarios():
    """
    Define advanced test scenarios for comprehensive algorithm evaluation.

    Focus areas:
    - Multi-machine scalability (3-4 machines)
    - Realistic workload patterns
    - Burst arrival handling
    - Load saturation scenarios
    - Practical applicability demonstration

    Returns:
        list: List of scenario dictionaries, each containing:
            - name (str): Scenario name
            - description (str): What the scenario tests
            - tasks (list): List of Task objects
            - num_machines (int): Number of parallel machines
    """

    scenarios = []

    # Advanced 1: Multi-Machine Load Balance
    scenarios.append({
        'name': 'Advanced 1: Multi-Machine Balance',
        'description': '4 machines with balanced workload - tests parallel efficiency',
        'tasks': [
            # Wave 1: 4 tasks (1 per machine)
            Task(1, 0, 3, Priority.HIGH, 15),
            Task(2, 0, 4, Priority.HIGH, 18),
            Task(3, 0, 3, Priority.LOW, 20),
            Task(4, 0, 4, Priority.LOW, 22),
            # Wave 2: 4 more tasks
            Task(5, 5, 3, Priority.HIGH, 25),
            Task(6, 5, 2, Priority.HIGH, 20),
            Task(7, 5, 5, Priority.LOW, 30),
            Task(8, 5, 3, Priority.LOW, 28),
            # Wave 3: Final 8 tasks
            Task(9, 10, 2, Priority.HIGH, 30),
            Task(10, 10, 3, Priority.HIGH, 32),
            Task(11, 10, 4, Priority.LOW, 35),
            Task(12, 10, 2, Priority.LOW, 33),
            Task(13, 12, 3, Priority.HIGH, 35),
            Task(14, 12, 2, Priority.HIGH, 33),
            Task(15, 12, 3, Priority.LOW, 40),
            Task(16, 12, 4, Priority.LOW, 42),
        ],
        'num_machines': 4
    })

    # Advanced 2: Machine Saturation
    scenarios.append({
        'name': 'Advanced 2: Machine Saturation',
        'description': 'Heavy overload - 20 tasks on 3 machines',
        'tasks': [
            # High-priority flood (15 tasks)
            Task(1, 0, 2, Priority.HIGH, 15),
            Task(2, 0, 3, Priority.HIGH, 18),
            Task(3, 1, 2, Priority.HIGH, 16),
            Task(4, 1, 3, Priority.HIGH, 19),
            Task(5, 2, 2, Priority.HIGH, 17),
            Task(6, 2, 3, Priority.HIGH, 20),
            Task(7, 3, 2, Priority.HIGH, 18),
            Task(8, 3, 3, Priority.HIGH, 21),
            Task(9, 4, 2, Priority.HIGH, 19),
            Task(10, 4, 3, Priority.HIGH, 22),
            Task(11, 5, 2, Priority.HIGH, 20),
            Task(12, 5, 3, Priority.HIGH, 23),
            Task(13, 6, 2, Priority.HIGH, 21),
            Task(14, 6, 3, Priority.HIGH, 24),
            Task(15, 7, 2, Priority.HIGH, 22),
            # Low-priority at risk (5 tasks)
            Task(16, 0, 4, Priority.LOW, 25),
            Task(17, 2, 5, Priority.LOW, 30),
            Task(18, 4, 4, Priority.LOW, 28),
            Task(19, 6, 5, Priority.LOW, 35),
            Task(20, 8, 4, Priority.LOW, 32),
        ],
        'num_machines': 3
    })

    # Advanced 3: Burst Arrival Pattern
    scenarios.append({
        'name': 'Advanced 3: Burst Arrival',
        'description': 'Quiet-burst-quiet pattern tests dynamic adaptation',
        'tasks': [
            # Quiet period: 2 tasks
            Task(1, 0, 3, Priority.HIGH, 12),
            Task(2, 0, 4, Priority.LOW, 18),
            # Sudden burst at t=5: 6 tasks arrive
            Task(3, 5, 2, Priority.HIGH, 15),
            Task(4, 5, 3, Priority.HIGH, 18),
            Task(5, 5, 2, Priority.HIGH, 16),
            Task(6, 5, 4, Priority.LOW, 22),
            Task(7, 5, 3, Priority.LOW, 20),
            Task(8, 5, 2, Priority.LOW, 19),
            # Recovery period at t=15: 4 tasks
            Task(9, 15, 3, Priority.HIGH, 30),
            Task(10, 15, 2, Priority.HIGH, 28),
            Task(11, 15, 4, Priority.LOW, 35),
            Task(12, 15, 3, Priority.LOW, 32),
        ],
        'num_machines': 2
    })

    # Advanced 4: Web Server Simulation
    scenarios.append({
        'name': 'Advanced 4: Web Server Workload',
        'description': 'Realistic: Quick API calls + batch reports',
        'tasks': [
            # Quick API requests (HIGH priority, short processing, tight deadlines)
            Task(1, 0, 1, Priority.HIGH, 5),
            Task(2, 1, 1, Priority.HIGH, 6),
            Task(3, 2, 2, Priority.HIGH, 9),
            Task(4, 3, 1, Priority.HIGH, 8),
            Task(5, 4, 2, Priority.HIGH, 11),
            Task(6, 5, 1, Priority.HIGH, 10),
            Task(7, 6, 2, Priority.HIGH, 13),
            Task(8, 7, 1, Priority.HIGH, 12),
            Task(9, 8, 1, Priority.HIGH, 13),
            Task(10, 9, 2, Priority.HIGH, 16),
            # Batch reports (LOW priority, long processing, loose deadlines)
            Task(11, 0, 6, Priority.LOW, 25),
            Task(12, 3, 7, Priority.LOW, 30),
            Task(13, 6, 8, Priority.LOW, 35),
        ],
        'num_machines': 2
    })

    # Advanced 5: Database Query Mix (OLTP + OLAP)
    scenarios.append({
        'name': 'Advanced 5: Database Workload',
        'description': 'OLTP transactions vs OLAP analytical queries',
        'tasks': [
            # OLTP: Transactional queries (HIGH, short, frequent)
            Task(1, 0, 1, Priority.HIGH, 8),
            Task(2, 1, 2, Priority.HIGH, 10),
            Task(3, 2, 1, Priority.HIGH, 9),
            Task(4, 3, 3, Priority.HIGH, 13),
            Task(5, 4, 2, Priority.HIGH, 12),
            Task(6, 5, 1, Priority.HIGH, 11),
            Task(7, 6, 2, Priority.HIGH, 14),
            Task(8, 7, 1, Priority.HIGH, 13),
            Task(9, 8, 3, Priority.HIGH, 17),
            Task(10, 9, 2, Priority.HIGH, 16),
            Task(11, 10, 1, Priority.HIGH, 15),
            Task(12, 11, 2, Priority.HIGH, 18),
            # OLAP: Analytical queries (LOW, long processing, loose deadlines)
            Task(13, 0, 10, Priority.LOW, 40),
            Task(14, 5, 12, Priority.LOW, 45),
        ],
        'num_machines': 2
    })

    return scenarios


"""
New Experimental Scenarios for Scheduling Research
==================================================

Additional scenarios to complement existing test suite:
1. Deadline Gradient - Progressive deadline pressure testing
2. Equal Priority - Tie-breaking behavior isolation
3. Periodic Pattern - Regular arrival predictability
4. Bimodal Processing - Extreme processing time variance
5. Overload Recovery - Algorithm recovery from saturation

Author: PySchedule Development Team
Date: 2024
"""



def get_new_experiments():
    """
    Returns list of new experimental scenarios.

    Each scenario tests a specific algorithmic characteristic not well-covered
    by existing Basic, Challenge, Extreme, and Advanced scenarios.
    """
    scenarios = []

    # ========================================================================
    # NEW 1: Deadline Gradient
    # ========================================================================
    # Purpose: Test DPE alpha sensitivity with continuous deadline pressure gradient
    # Design: 10 tasks with progressively tightening deadlines (loose → tight)
    # Expected: DPE should elevate tasks as pressure increases, EDF handles naturally
    scenarios.append({
        'name': 'New 1: Deadline Gradient',
        'description': 'Progressive deadline tightening - tests DPE elevation timing',
        'tasks': [
            # Very loose deadlines (5x processing time)
            Task(1, 0, 3, Priority.LOW, 15),    # pressure = 0.2
            Task(2, 0, 3, Priority.LOW, 15),    # pressure = 0.2

            # Loose deadlines (4x processing time)
            Task(3, 2, 3, Priority.LOW, 14),    # pressure → 0.25
            Task(4, 2, 3, Priority.LOW, 14),    # pressure → 0.25

            # Moderate deadlines (3x processing time)
            Task(5, 4, 3, Priority.LOW, 13),    # pressure → 0.33
            Task(6, 4, 3, Priority.LOW, 13),    # pressure → 0.33

            # Tight deadlines (2x processing time)
            Task(7, 6, 3, Priority.LOW, 12),    # pressure → 0.5
            Task(8, 6, 3, Priority.LOW, 12),    # pressure → 0.5

            # Very tight deadlines (1.5x processing time)
            Task(9, 8, 3, Priority.LOW, 12),    # pressure → 0.67
            Task(10, 8, 3, Priority.LOW, 12),   # pressure → 0.67
        ],
        'num_machines': 2
    })

    # ========================================================================
    # NEW 2: Equal Priority Mix
    # ========================================================================
    # Purpose: Test tie-breaking behavior when priorities don't differentiate
    # Design: 8 HIGH priority tasks with varying deadlines
    # Expected: EDF should perform well, Priority-First/SPT rely on secondary criteria
    scenarios.append({
        'name': 'New 2: Equal Priority Mix',
        'description': 'All HIGH priority - tests tie-breaking by deadline/processing time',
        'tasks': [
            Task(1, 0, 5, Priority.HIGH, 20),   # Long task, loose deadline
            Task(2, 0, 2, Priority.HIGH, 10),   # Short task, tight deadline
            Task(3, 1, 4, Priority.HIGH, 18),   # Medium task, moderate deadline
            Task(4, 1, 3, Priority.HIGH, 15),   # Medium task, moderate deadline
            Task(5, 3, 6, Priority.HIGH, 25),   # Long task, loose deadline
            Task(6, 3, 1, Priority.HIGH, 8),    # Very short task, tight deadline
            Task(7, 5, 3, Priority.HIGH, 20),   # Medium task, loose deadline
            Task(8, 5, 2, Priority.HIGH, 12),   # Short task, moderate deadline
        ],
        'num_machines': 2
    })

    # ========================================================================
    # NEW 3: Periodic Arrivals
    # ========================================================================
    # Purpose: Test algorithm behavior with regular, predictable arrival pattern
    # Design: Tasks arriving every 3 time units, mixed priorities
    # Expected: All algorithms should handle well, tests predictability advantage
    scenarios.append({
        'name': 'New 3: Periodic Arrivals',
        'description': 'Regular arrival pattern every 3 time units - tests predictability',
        'tasks': [
            # Period 1 (t=0)
            Task(1, 0, 3, Priority.HIGH, 12),
            Task(2, 0, 2, Priority.LOW, 15),

            # Period 2 (t=3)
            Task(3, 3, 3, Priority.HIGH, 15),
            Task(4, 3, 2, Priority.LOW, 18),

            # Period 3 (t=6)
            Task(5, 6, 3, Priority.HIGH, 18),
            Task(6, 6, 2, Priority.LOW, 21),

            # Period 4 (t=9)
            Task(7, 9, 3, Priority.HIGH, 21),
            Task(8, 9, 2, Priority.LOW, 24),

            # Period 5 (t=12)
            Task(9, 12, 3, Priority.HIGH, 24),
            Task(10, 12, 2, Priority.LOW, 27),
        ],
        'num_machines': 2
    })

    # ========================================================================
    # NEW 4: Bimodal Processing Times
    # ========================================================================
    # Purpose: Test handling of extreme processing time variance
    # Design: Mix of very short (1-2) and very long (10-12) tasks
    # Expected: SPT favors short tasks heavily, may starve long tasks
    scenarios.append({
        'name': 'New 4: Bimodal Processing',
        'description': 'Extreme processing time variance - tests SPT bias',
        'tasks': [
            # Very short tasks
            Task(1, 0, 1, Priority.HIGH, 10),
            Task(2, 0, 2, Priority.HIGH, 12),
            Task(3, 1, 1, Priority.LOW, 15),
            Task(4, 1, 2, Priority.LOW, 18),

            # Very long tasks
            Task(5, 2, 10, Priority.HIGH, 30),
            Task(6, 2, 12, Priority.HIGH, 35),
            Task(7, 3, 10, Priority.LOW, 35),
            Task(8, 3, 12, Priority.LOW, 40),

            # More short tasks arriving later
            Task(9, 5, 1, Priority.HIGH, 20),
            Task(10, 5, 2, Priority.HIGH, 22),
        ],
        'num_machines': 2
    })

    # ========================================================================
    # NEW 5: Overload Recovery
    # ========================================================================
    # Purpose: Test algorithm recovery from initial saturation
    # Design: Heavy load at start (15 tasks, 0-2 arrival), then gradual reduction
    # Expected: DPE/EDF should recover better, SPT/Priority may accumulate misses
    scenarios.append({
        'name': 'New 5: Overload Recovery',
        'description': 'Heavy initial load then reduction - tests recovery from saturation',
        'tasks': [
            # Heavy initial load (15 tasks arriving t=0-2)
            Task(1, 0, 3, Priority.HIGH, 15),
            Task(2, 0, 3, Priority.HIGH, 15),
            Task(3, 0, 2, Priority.LOW, 20),
            Task(4, 0, 2, Priority.LOW, 20),
            Task(5, 1, 3, Priority.HIGH, 16),
            Task(6, 1, 3, Priority.HIGH, 16),
            Task(7, 1, 2, Priority.LOW, 21),
            Task(8, 1, 2, Priority.LOW, 21),
            Task(9, 2, 3, Priority.HIGH, 17),
            Task(10, 2, 3, Priority.HIGH, 17),
            Task(11, 2, 2, Priority.LOW, 22),
            Task(12, 2, 2, Priority.LOW, 22),
            Task(13, 2, 2, Priority.LOW, 22),
            Task(14, 2, 2, Priority.LOW, 22),
            Task(15, 2, 2, Priority.LOW, 22),

            # Gradual reduction (3 tasks later)
            Task(16, 10, 2, Priority.HIGH, 25),
            Task(17, 12, 2, Priority.LOW, 28),
            Task(18, 14, 2, Priority.HIGH, 30),
        ],
        'num_machines': 3
    })

    return scenarios


if __name__ == "__main__":
    """Test scenario creation"""
    scenarios = get_new_experiments()
    print(f"\n{'='*80}")
    print(f"NEW EXPERIMENTAL SCENARIOS")
    print(f"{'='*80}\n")

    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Tasks: {len(scenario['tasks'])}")
        print(f"   Machines: {scenario['num_machines']}")
        print()

    print(f"{'='*80}")
    print(f"Total new scenarios: {len(scenarios)}")
    print(f"These complement existing 19 scenarios")
    print(f"New total: {19 + len(scenarios)} scenarios")
    print(f"New total experiments: {(19 + len(scenarios)) * 7} (with 7 algorithms)")
    print(f"{'='*80}")
