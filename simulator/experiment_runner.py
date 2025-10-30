"""
Experiment Runner for COMP3821 Scheduling Project
===================================================

This script helps you:
1. Define test scenarios
2. Run multiple algorithms
3. Collect metrics automatically
4. Export results to CSV for analysis
"""

import csv
import copy
from simple_simulator import (
    Task, Priority, 
    SPT_Scheduler, EDF_Scheduler, 
    PriorityFirst_Scheduler, DPE_Scheduler
)


class ExperimentRunner:
    """Run and track scheduling experiments"""
    
    def __init__(self):
        self.results = []
    
    def create_scenario(self, name, tasks, num_machines, description=""):
        """Create a test scenario"""
        return {
            'name': name,
            'description': description,
            'tasks': tasks,
            'num_machines': num_machines
        }
    
    def run_experiment(self, scenario, algorithm_name, SchedulerClass, **kwargs):
        """Run single experiment and collect metrics"""
        print(f"\n🔬 Running: {algorithm_name} on {scenario['name']}")
        
        # Create fresh task copies
        tasks = copy.deepcopy(scenario['tasks'])
        
        # Run scheduler
        scheduler = SchedulerClass(tasks, scenario['num_machines'], **kwargs)
        scheduler.run()
        
        # Calculate metrics
        metrics = self.calculate_metrics(
            tasks, 
            scenario['name'], 
            algorithm_name,
            scheduler.current_time
        )
        
        # Store results
        self.results.append(metrics)
        
        # Print summary
        self.print_summary(metrics)
        
        return metrics
    
    def calculate_metrics(self, tasks, scenario_name, algorithm_name, sim_time):
        """Calculate all relevant metrics"""
        
        # Basic counts
        total_tasks = len(tasks)
        high_priority = [t for t in tasks if t.priority == Priority.HIGH]
        low_priority = [t for t in tasks if t.priority == Priority.LOW]
        
        # Deadline metrics
        high_met = sum(1 for t in high_priority if t.meets_deadline())
        low_met = sum(1 for t in low_priority if t.meets_deadline())
        total_met = high_met + low_met
        
        # Time metrics
        makespan = max((t.completion_time for t in tasks if t.completion_time), default=0)
        
        response_times = [t.completion_time - t.arrival_time 
                         for t in tasks if t.completion_time]
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        waiting_times = [t.start_time - t.arrival_time 
                        for t in tasks if t.start_time]
        avg_waiting = sum(waiting_times) / len(waiting_times) if waiting_times else 0
        
        # Success rates
        high_success_rate = (high_met / len(high_priority) * 100) if high_priority else 0
        low_success_rate = (low_met / len(low_priority) * 100) if low_priority else 0
        total_success_rate = (total_met / total_tasks * 100) if total_tasks else 0
        
        return {
            'Scenario': scenario_name,
            'Algorithm': algorithm_name,
            'Total Tasks': total_tasks,
            'High Priority Tasks': len(high_priority),
            'Low Priority Tasks': len(low_priority),
            'High Met Deadline': high_met,
            'Low Met Deadline': low_met,
            'Total Met Deadline': total_met,
            'High Success Rate (%)': round(high_success_rate, 2),
            'Low Success Rate (%)': round(low_success_rate, 2),
            'Total Success Rate (%)': round(total_success_rate, 2),
            'Makespan': round(makespan, 2),
            'Avg Response Time': round(avg_response, 2),
            'Avg Waiting Time': round(avg_waiting, 2),
            'Simulation Time': round(sim_time, 2)
        }
    
    def print_summary(self, metrics):
        """Print metrics summary"""
        print(f"  ✓ Success Rate: {metrics['Total Success Rate (%)']:.1f}%")
        print(f"  ✓ High Priority: {metrics['High Success Rate (%)']:.1f}%")
        print(f"  ✓ Low Priority: {metrics['Low Success Rate (%)']:.1f}%")
        print(f"  ⏱ Makespan: {metrics['Makespan']:.1f}")
    
    def export_to_csv(self, filename='experiment_results.csv'):
        """Export all results to CSV"""
        if not self.results:
            print("No results to export!")
            return
        
        keys = self.results[0].keys()
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"\n📊 Results exported to: {filename}")
    
    def compare_algorithms(self):
        """Print comparison table"""
        if not self.results:
            print("No results to compare!")
            return
        
        print("\n" + "=" * 100)
        print("COMPARISON TABLE")
        print("=" * 100)
        
        # Group by scenario
        scenarios = {}
        for result in self.results:
            scenario = result['Scenario']
            if scenario not in scenarios:
                scenarios[scenario] = []
            scenarios[scenario].append(result)
        
        for scenario_name, results in scenarios.items():
            print(f"\n{scenario_name}:")
            print("-" * 100)
            print(f"{'Algorithm':<20} | {'Success%':<10} | {'High%':<10} | {'Low%':<10} | {'Makespan':<10}")
            print("-" * 100)
            
            for r in results:
                print(f"{r['Algorithm']:<20} | "
                      f"{r['Total Success Rate (%)']:<10.1f} | "
                      f"{r['High Success Rate (%)']:<10.1f} | "
                      f"{r['Low Success Rate (%)']:<10.1f} | "
                      f"{r['Makespan']:<10.1f}")


# =============================================================================
# TEST SCENARIOS
# =============================================================================

def get_test_scenarios():
    """Define all test scenarios here"""
    
    scenarios = []
    
    # Scenario 1: Light Load (Easy)
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
    
    # Scenario 4: All arrive together
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

# =============================================================================
# CHALLENGING TEST CASES (Add after get_test_scenarios)
# =============================================================================

def get_challenging_scenarios():
    """Challenging test scenarios that reveal algorithm differences"""
    
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


# =============================================================================
# EXTREME TEST CASES
# =============================================================================

def get_extreme_scenarios():
    """Extreme test scenarios designed to maximize differences"""
    
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

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

def run_all_experiments():
    """Run complete experimental suite including challenging and extreme cases"""
    
    runner = ExperimentRunner()
    
    # Get all scenarios
    basic_scenarios = get_test_scenarios()
    challenging_scenarios = get_challenging_scenarios()
    extreme_scenarios = get_extreme_scenarios()
    
    all_scenarios = basic_scenarios + challenging_scenarios + extreme_scenarios
    
    # Define algorithms to test
    algorithms = [
        ('SPT', SPT_Scheduler, {}),
        ('EDF', EDF_Scheduler, {}),
        ('Priority-First', PriorityFirst_Scheduler, {}),
        ('DPE (α=0.5)', DPE_Scheduler, {'alpha': 0.5}),
        ('DPE (α=0.7)', DPE_Scheduler, {'alpha': 0.7}),
        ('DPE (α=0.9)', DPE_Scheduler, {'alpha': 0.9}),
    ]
    
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "RUNNING COMPREHENSIVE EXPERIMENTS" + " " * 30 + "║")
    print("║" + " " * 10 + f"Basic: {len(basic_scenarios)} | Challenging: {len(challenging_scenarios)} | Extreme: {len(extreme_scenarios)}" + " " * 10 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Run experiments
    for scenario in all_scenarios:
        print(f"\n\n{'=' * 80}")
        print(f"SCENARIO: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Tasks: {len(scenario['tasks'])}, Machines: {scenario['num_machines']}")
        print('=' * 80)
        
        for algo_name, SchedulerClass, kwargs in algorithms:
            runner.run_experiment(scenario, algo_name, SchedulerClass, **kwargs)
    
    # Print comparison
    runner.compare_algorithms()
    
    # Export results
    runner.export_to_csv('comprehensive_results.csv')
    
    print("\n" + "=" * 80)
    print("✅ ALL EXPERIMENTS COMPLETE!")
    print("=" * 80)
    print(f"\nTotal scenarios tested: {len(all_scenarios)}")
    print(f"  • Basic: {len(basic_scenarios)}")
    print(f"  • Challenging: {len(challenging_scenarios)}")
    print(f"  • Extreme: {len(extreme_scenarios)}")
    print(f"\nTotal experiments run: {len(all_scenarios) * len(algorithms)}")
    print("\nResults saved to: comprehensive_results.csv")
    print("\nNext steps:")
    print("1. Open comprehensive_results.csv in Excel/Google Sheets")
    print("2. Create charts comparing algorithms")
    print("3. Analyze when DPE helps vs hurts")
    print("4. Focus on 'Challenging' and 'Extreme' scenarios for your report")
    print("=" * 80)

if __name__ == "__main__":
    run_all_experiments()