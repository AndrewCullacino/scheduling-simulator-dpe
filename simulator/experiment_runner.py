"""
Experiment Runner for COMP3821 Scheduling Project
===================================================

This script helps you:
1. Run test scenarios from organized scenario files
2. Execute multiple algorithms
3. Collect metrics automatically
4. Export results to CSV for analysis

Scenarios are organized in separate files:
- simple_scenarios.py: Basic validation scenarios
- challenge_scenarios.py: Scenarios revealing algorithm differences
- extreme_scenarios.py: Extreme stress test scenarios
"""

import csv
import copy
from simple_simulator import (
    Task, Priority,
    SPT_Scheduler, EDF_Scheduler,
    PriorityFirst_Scheduler, DPE_Scheduler
)
from simple_scenarios import get_simple_scenarios
from challenge_scenarios import get_challenge_scenarios
from extreme_scenarios import get_extreme_scenarios


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
    
    def export_to_csv(self, filename='results/experiment_results.csv'):
        """Export all results to CSV in results/ folder"""
        if not self.results:
            print("No results to export!")
            return

        # Ensure results directory exists
        import os
        os.makedirs('results', exist_ok=True)

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
# SCENARIOS NOW IMPORTED FROM SEPARATE FILES
# =============================================================================
# Simple scenarios: simple_scenarios.py
# Challenge scenarios: challenge_scenarios.py
# Extreme scenarios: extreme_scenarios.py

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

def run_all_experiments():
    """Run complete experimental suite including challenging and extreme cases"""

    runner = ExperimentRunner()

    # Get all scenarios from organized scenario files
    basic_scenarios = get_simple_scenarios()
    challenging_scenarios = get_challenge_scenarios()
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
    runner.export_to_csv('results/comprehensive_results.csv')

    print("\n" + "=" * 80)
    print("✅ ALL EXPERIMENTS COMPLETE!")
    print("=" * 80)
    print(f"\nTotal scenarios tested: {len(all_scenarios)}")
    print(f"  • Basic: {len(basic_scenarios)}")
    print(f"  • Challenging: {len(challenging_scenarios)}")
    print(f"  • Extreme: {len(extreme_scenarios)}")
    print(f"\nTotal experiments run: {len(all_scenarios) * len(algorithms)}")
    print("\nResults saved to: results/comprehensive_results.csv")
    print("\nNext steps:")
    print("1. Open results/comprehensive_results.csv in Excel/Google Sheets")
    print("2. Create charts comparing algorithms")
    print("3. Analyze when DPE helps vs hurts")
    print("4. Focus on 'Challenging' and 'Extreme' scenarios for your report")
    print("=" * 80)

if __name__ == "__main__":
    run_all_experiments()