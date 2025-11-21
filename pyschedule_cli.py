#!/usr/bin/env python3
"""
PySchedule Command-Line Interface

Professional CLI for running scheduling experiments and generating analysis.

Usage:
    python pyschedule_cli.py run --all
    python pyschedule_cli.py run --algorithm SPT --scenario simple_1
    python pyschedule_cli.py list algorithms
    python pyschedule_cli.py analyze results/experiment_results.csv
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from simple_simulator import Task, Priority
from algorithms import get_all_algorithms
from scenarios import get_all_scenarios
from runner import ExperimentRunner, run_all_experiments


def list_algorithms():
    """List all available scheduling algorithms."""
    algorithms = get_all_algorithms()

    print("\n" + "=" * 60)
    print("AVAILABLE SCHEDULING ALGORITHMS")
    print("=" * 60)

    print("\n📊 Greedy Algorithms:")
    print("  • SPT - Shortest Processing Time First")
    print("  • EDF - Earliest Deadline First")

    print("\n🎯 Priority-Based Algorithms:")
    print("  • Priority-First - Static priority with EDF tiebreaking")

    print("\n🔄 Adaptive Algorithms:")
    print("  • DPE (α=0.3) - Dynamic Priority Elevation (conservative)")
    print("  • DPE (α=0.5) - Dynamic Priority Elevation (balanced)")
    print("  • DPE (α=0.7) - Dynamic Priority Elevation (moderate)")
    print("  • DPE (α=0.9) - Dynamic Priority Elevation (aggressive)")

    print(f"\nTotal: {len(algorithms)} algorithm variants")
    print("=" * 60 + "\n")


def list_scenarios():
    """List all available test scenarios."""
    scenarios = get_all_scenarios()

    print("\n" + "=" * 60)
    print("AVAILABLE TEST SCENARIOS")
    print("=" * 60)

    categories = {
        'Simple': [],
        'Challenge': [],
        'Extreme': [],
        'Advanced': [],
        'New': []
    }

    for scenario in scenarios:
        name = scenario['name']
        for category in categories.keys():
            if category in name:
                categories[category].append(scenario)
                break

    for category, scenarios_list in categories.items():
        if scenarios_list:
            print(f"\n{category} Scenarios ({len(scenarios_list)}):")
            for scenario in scenarios_list:
                print(f"  • {scenario['name']}")
                print(f"    Tasks: {len(scenario['tasks'])}, Machines: {scenario['num_machines']}")

    print(f"\nTotal: {len(scenarios)} scenarios")
    print("=" * 60 + "\n")


def run_single_experiment(algorithm_name: str, scenario_name: str, output_dir: str = "results"):
    """Run a single algorithm/scenario combination."""
    algorithms = get_all_algorithms()
    scenarios = get_all_scenarios()

    # Validate algorithm
    if algorithm_name not in algorithms:
        print(f"❌ Error: Algorithm '{algorithm_name}' not found.")
        print(f"Available algorithms: {', '.join(algorithms.keys())}")
        return 1

    # Find scenario
    scenario = next((s for s in scenarios if s['name'] == scenario_name), None)
    if not scenario:
        print(f"❌ Error: Scenario '{scenario_name}' not found.")
        print(f"Use 'pyschedule_cli.py list scenarios' to see available scenarios.")
        return 1

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Run experiment
    print(f"\n🔬 Running experiment:")
    print(f"  Algorithm: {algorithm_name}")
    print(f"  Scenario: {scenario['name']}")
    print(f"  Output: {output_dir}/")
    print()

    runner = ExperimentRunner()
    metrics = runner.run_experiment(
        scenario=scenario,
        algorithm_name=algorithm_name,
        SchedulerClass=algorithms[algorithm_name]
    )

    # Export results
    output_file = f"{output_dir}/single_experiment_{algorithm_name}_{scenario_name}.csv"
    runner.export_to_csv(output_file)

    print(f"\n✅ Experiment complete!")
    print(f"Results saved to: {output_file}")
    return 0


def run_all(output_dir: str = "results"):
    """Run all experiments (all algorithms × all scenarios)."""
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE EXPERIMENTAL SUITE")
    print("=" * 60)

    algorithms = get_all_algorithms()
    scenarios = get_all_scenarios()

    print(f"\nConfiguration:")
    print(f"  Algorithms: {len(algorithms)}")
    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Total experiments: {len(algorithms) * len(scenarios)}")
    print(f"  Output directory: {output_dir}/")
    print()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Run all experiments
    run_all_experiments()

    print("\n✅ All experiments complete!")
    print(f"Results saved to: {output_dir}/comprehensive_results.csv")
    return 0


def run_by_algorithm(algorithm_name: str, output_dir: str = "results"):
    """Run single algorithm across all scenarios."""
    algorithms = get_all_algorithms()
    scenarios = get_all_scenarios()

    if algorithm_name not in algorithms:
        print(f"❌ Error: Algorithm '{algorithm_name}' not found.")
        print(f"Available algorithms: {', '.join(algorithms.keys())}")
        return 1

    print(f"\n🔬 Running {algorithm_name} across all scenarios...")
    print(f"Total scenarios: {len(scenarios)}\n")

    os.makedirs(output_dir, exist_ok=True)

    runner = ExperimentRunner()
    for scenario in scenarios:
        runner.run_experiment(
            scenario=scenario,
            algorithm_name=algorithm_name,
            SchedulerClass=algorithms[algorithm_name]
        )

    # Calculate composite scores and export
    runner.calculate_composite_scores()
    output_file = f"{output_dir}/{algorithm_name}_all_scenarios.csv"
    runner.export_to_csv(output_file)

    print(f"\n✅ {algorithm_name} experiments complete!")
    print(f"Results saved to: {output_file}")
    return 0


def run_by_scenario(scenario_name: str, output_dir: str = "results"):
    """Run all algorithms on single scenario."""
    algorithms = get_all_algorithms()
    scenarios = get_all_scenarios()

    scenario = next((s for s in scenarios if s['name'] == scenario_name), None)
    if not scenario:
        print(f"❌ Error: Scenario '{scenario_name}' not found.")
        return 1

    print(f"\n🔬 Running all algorithms on: {scenario['name']}")
    print(f"Total algorithms: {len(algorithms)}\n")

    os.makedirs(output_dir, exist_ok=True)

    runner = ExperimentRunner()
    for algo_name, algo_class in algorithms.items():
        runner.run_experiment(
            scenario=scenario,
            algorithm_name=algo_name,
            SchedulerClass=algo_class
        )

    # Calculate composite scores and comparison
    runner.calculate_composite_scores()
    runner.compare_algorithms()

    output_file = f"{output_dir}/{scenario_name}_all_algorithms.csv"
    runner.export_to_csv(output_file)

    print(f"\n✅ Scenario experiments complete!")
    print(f"Results saved to: {output_file}")
    return 0


def analyze_results(results_file: str):
    """Analyze and summarize experiment results from CSV."""
    import pandas as pd

    if not os.path.exists(results_file):
        print(f"❌ Error: Results file not found: {results_file}")
        return 1

    print(f"\n📊 Analyzing results from: {results_file}\n")

    df = pd.read_csv(results_file)

    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    print(f"\nTotal experiments: {len(df)}")
    print(f"Algorithms tested: {df['Algorithm'].nunique()}")
    print(f"Scenarios tested: {df['Scenario'].nunique()}")

    print("\n📈 Overall Performance Metrics:")
    print(f"  Average Success Rate: {df['Total Success Rate (%)'].mean():.2f}%")
    print(f"  Average High Priority Success: {df['High Success Rate (%)'].mean():.2f}%")
    print(f"  Average Low Priority Success: {df['Low Success Rate (%)'].mean():.2f}%")

    print("\n🏆 Best Performing Algorithm (by success rate):")
    best_algo = df.groupby('Algorithm')['Total Success Rate (%)'].mean().idxmax()
    best_success = df.groupby('Algorithm')['Total Success Rate (%)'].mean().max()
    print(f"  {best_algo}: {best_success:.2f}%")

    print("\n⚡ Fastest Algorithm (by makespan):")
    fastest_algo = df.groupby('Algorithm')['Makespan'].mean().idxmin()
    fastest_makespan = df.groupby('Algorithm')['Makespan'].mean().min()
    print(f"  {fastest_algo}: {fastest_makespan:.2f} time units")

    print("\n" + "=" * 70 + "\n")
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PySchedule: Real-Time Scheduling Research Toolkit CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available options
  %(prog)s list algorithms
  %(prog)s list scenarios

  # Run experiments
  %(prog)s run --all
  %(prog)s run --algorithm SPT --scenario "Simple Scenario 1"
  %(prog)s run --by-algorithm EDF
  %(prog)s run --by-scenario "Challenge Scenario 1"

  # Analyze results
  %(prog)s analyze results/comprehensive_results.csv
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List available algorithms or scenarios')
    list_parser.add_argument('item', choices=['algorithms', 'scenarios'],
                            help='What to list')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run scheduling experiments')
    run_group = run_parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument('--all', action='store_true',
                          help='Run all algorithms on all scenarios')
    run_group.add_argument('--algorithm', type=str,
                          help='Specific algorithm to run')
    run_group.add_argument('--by-algorithm', type=str,
                          help='Run single algorithm across all scenarios')
    run_group.add_argument('--by-scenario', type=str,
                          help='Run all algorithms on single scenario')

    run_parser.add_argument('--scenario', type=str,
                           help='Specific scenario (required with --algorithm)')
    run_parser.add_argument('--output', type=str, default='results',
                           help='Output directory (default: results/)')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze experiment results')
    analyze_parser.add_argument('results_file', type=str,
                               help='Path to results CSV file')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Execute commands
    if args.command == 'list':
        if args.item == 'algorithms':
            list_algorithms()
        elif args.item == 'scenarios':
            list_scenarios()
        return 0

    elif args.command == 'run':
        if args.all:
            return run_all(args.output)
        elif args.by_algorithm:
            return run_by_algorithm(args.by_algorithm, args.output)
        elif args.by_scenario:
            return run_by_scenario(args.by_scenario, args.output)
        elif args.algorithm:
            if not args.scenario:
                print("❌ Error: --scenario required when using --algorithm")
                return 1
            return run_single_experiment(args.algorithm, args.scenario, args.output)

    elif args.command == 'analyze':
        return analyze_results(args.results_file)

    return 0


if __name__ == '__main__':
    sys.exit(main())
