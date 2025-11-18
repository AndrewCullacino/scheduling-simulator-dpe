"""
Generate All Visualizations for Final Report
=============================================

This script generates all publication-quality visualizations needed for:
1. Final report (10 pages)
2. Poster presentation

Reads data from results/comprehensive_results.csv and generates:
- Gantt charts for key scenarios
- Performance comparison charts
- Success rate visualizations
- Statistical analysis plots
- Summary heatmaps
"""

import pandas as pd
import copy
from simple_simulator import (
    Task, Priority,
    SPT_Scheduler, EDF_Scheduler,
    PriorityFirst_Scheduler, DPE_Scheduler
)
from enhanced_visualizations import SchedulingVisualizer
from challenge_tasks import *
import os


def load_results_data(csv_file='results/comprehensive_results.csv'):
    """Load experimental results from CSV"""
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print(f"✅ Loaded {len(df)} results from {csv_file}")
        return df
    else:
        print(f"❌ File not found: {csv_file}")
        return None


def generate_key_gantt_charts(viz):
    """
    Generate Gantt charts for scenarios showing algorithm differences.

    Focus on:
    1. Batch Arrival (SPT vs others)
    2. Challenge 4 (EDF vs others)
    3. Challenge 5 (Priority inversion)
    """
    print("\n" + "=" * 70)
    print("GENERATING KEY GANTT CHARTS")
    print("=" * 70)

    # Scenario 1: Batch Arrival - Shows SPT advantage
    # MUST match experiment_runner.py lines 220-232
    print("\n1. Batch Arrival Scenario...")
    tasks_batch = [
        Task(1, 0, 3, Priority.HIGH, 8),
        Task(2, 0, 4, Priority.HIGH, 10),
        Task(3, 0, 2, Priority.HIGH, 12),
        Task(4, 0, 5, Priority.LOW, 20),
        Task(5, 0, 6, Priority.LOW, 25),
        Task(6, 0, 3, Priority.LOW, 22),
    ]

    algorithms = [
        ("SPT", SPT_Scheduler),
        ("EDF", EDF_Scheduler),
        ("Priority-First", PriorityFirst_Scheduler),
        ("DPE (α=0.7)", lambda t, m: DPE_Scheduler(t, m, alpha=0.7)),
    ]

    for algo_name, SchedulerClass in algorithms:
        tasks_copy = copy.deepcopy(tasks_batch)
        scheduler = SchedulerClass(tasks_copy, 2)
        scheduler.run()
        viz.create_gantt_chart(tasks_copy, algo_name, "Batch Arrival", num_machines=2)

    # Scenario 2: Extreme 3 - Shows EDF advantage over SPT
    # MUST match experiment_runner.py lines 357-368
    print("\n2. Extreme 3 Scenario (SPT Fails)...")
    tasks_ext3 = [
        Task(1, 0, 1, Priority.HIGH, 50),
        Task(2, 0, 10, Priority.HIGH, 11),
        Task(3, 0, 2, Priority.HIGH, 45),
        Task(4, 0, 5, Priority.HIGH, 7),
    ]

    for algo_name, SchedulerClass in algorithms:
        tasks_copy = copy.deepcopy(tasks_ext3)
        scheduler = SchedulerClass(tasks_copy, 2)
        scheduler.run()
        viz.create_gantt_chart(tasks_copy, algo_name, "Extreme_3", num_machines=2)

    # Scenario 3: Challenge 4 - Alpha sensitivity
    # MUST match experiment_runner.py lines 287-298
    print("\n3. Challenge 4 Scenario (Alpha Matters)...")
    tasks_ch4 = [
        Task(1, 0, 4, Priority.LOW, 12),
        Task(2, 0, 2, Priority.HIGH, 20),
        Task(3, 1, 2, Priority.HIGH, 22),
        Task(4, 2, 2, Priority.HIGH, 24),
        Task(5, 1, 3, Priority.LOW, 15),
    ]

    for algo_name, SchedulerClass in algorithms:
        tasks_copy = copy.deepcopy(tasks_ch4)
        scheduler = SchedulerClass(tasks_copy, 2)
        scheduler.run()
        viz.create_gantt_chart(tasks_copy, algo_name, "Challenge_4", num_machines=2)

    # Scenario 4: Challenge 5 - Priority Inversion
    # MUST match experiment_runner.py lines 301-310
    print("\n4. Challenge 5 (Priority Inversion)...")
    tasks_ch5 = [
        Task(1, 0, 8, Priority.LOW, 30),
        Task(2, 2, 3, Priority.HIGH, 6),
        Task(3, 3, 2, Priority.HIGH, 8),
    ]

    for algo_name, SchedulerClass in algorithms:
        tasks_copy = copy.deepcopy(tasks_ch5)
        scheduler = SchedulerClass(tasks_copy, 1)
        scheduler.run()
        viz.create_gantt_chart(tasks_copy, algo_name, "Challenge_5", num_machines=1)

    print("\n✅ Key Gantt charts generated!")


def generate_performance_charts(viz, results_df):
    """Generate performance comparison charts from results CSV"""
    print("\n" + "=" * 70)
    print("GENERATING PERFORMANCE COMPARISON CHARTS")
    print("=" * 70)

    if results_df is None:
        print("⚠️ No results data available, skipping...")
        return

    # Chart 1: Makespan comparison
    print("\n1. Makespan comparison...")
    viz.create_makespan_comparison_detailed(results_df)

    # Chart 2: Success rates
    print("\n2. Success rate comparison...")
    viz.create_success_rate_stacked_bar(results_df)

    # Chart 3: Summary heatmap
    print("\n3. Algorithm summary heatmap...")
    viz.create_algorithm_summary_heatmap(results_df)

    print("\n✅ Performance charts generated!")


def generate_dpe_analysis_plots(viz):
    """Generate DPE-specific analysis visualizations"""
    print("\n" + "=" * 70)
    print("GENERATING DPE ANALYSIS PLOTS")
    print("=" * 70)

    # Create scenario with observable deadline pressure
    print("\n1. Deadline pressure evolution plot...")
    tasks_pressure = [
        Task(1, 0, 4, Priority.LOW, 20),
        Task(2, 0, 3, Priority.HIGH, 30),
        Task(3, 3, 3, Priority.HIGH, 35),
        Task(4, 1, 3, Priority.LOW, 18),
    ]

    # Run DPE to get actual scheduling
    tasks_copy = copy.deepcopy(tasks_pressure)
    scheduler = DPE_Scheduler(tasks_copy, 1, alpha=0.7)
    scheduler.run()

    # Generate pressure plot
    viz.create_deadline_pressure_plot(tasks_copy, alpha_threshold=0.7)

    # Test different alpha values
    print("\n2. Alpha sensitivity analysis...")
    alphas = [0.5, 0.7, 0.9]
    for alpha in alphas:
        tasks_copy = copy.deepcopy(tasks_pressure)
        scheduler = DPE_Scheduler(tasks_copy, 1, alpha=alpha)
        scheduler.run()
        viz.create_deadline_pressure_plot(tasks_copy, alpha_threshold=alpha)

    print("\n✅ DPE analysis plots generated!")


def generate_statistical_plots(viz):
    """Generate statistical distribution plots"""
    print("\n" + "=" * 70)
    print("GENERATING STATISTICAL ANALYSIS PLOTS")
    print("=" * 70)

    # Create test scenario with varied processing times
    print("\n1. Response time box plot...")
    test_tasks = [
        Task(i, 0, np.random.randint(1, 6), Priority.HIGH, 30)
        for i in range(10)
    ] + [
        Task(i+10, 0, np.random.randint(1, 6), Priority.LOW, 40)
        for i in range(10)
    ]

    # Run all algorithms
    all_results = {}
    algorithms = [
        ("SPT", SPT_Scheduler),
        ("EDF", EDF_Scheduler),
        ("Priority-First", PriorityFirst_Scheduler),
        ("DPE", lambda t, m: DPE_Scheduler(t, m, alpha=0.7)),
    ]

    for algo_name, SchedulerClass in algorithms:
        tasks_copy = copy.deepcopy(test_tasks)
        scheduler = SchedulerClass(tasks_copy, 2)
        scheduler.run()
        all_results[algo_name] = tasks_copy

    viz.create_response_time_boxplot(all_results)

    print("\n✅ Statistical plots generated!")


def create_comprehensive_report_figures():
    """Main function to generate all figures for final report"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║      COMPREHENSIVE VISUALIZATION GENERATION FOR FINAL REPORT   ║
║                                                                ║
║  This will create ALL publication-quality visualizations for:  ║
║  • Final 10-page report                                       ║
║  • Poster presentation                                        ║
║                                                                ║
║  Output directory: visualizations/                            ║
║  Estimated time: 2-3 minutes                                  ║
╚════════════════════════════════════════════════════════════════╝
    """)

    # Initialize visualizer
    viz = SchedulingVisualizer(output_dir='visualizations')

    # Load results data
    results_df = load_results_data('comprehensive_results.csv')

    # Generate all visualizations
    try:
        # 1. Gantt charts showing algorithm differences
        generate_key_gantt_charts(viz)

        # 2. Performance comparison charts
        generate_performance_charts(viz, results_df)

        # 3. DPE-specific analysis
        generate_dpe_analysis_plots(viz)

        # 4. Statistical analysis
        #generate_statistical_plots(viz)  # Disabled if no numpy

    except Exception as e:
        print(f"\n❌ Error during visualization generation: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("✨ VISUALIZATION GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nGenerated files in: visualizations/")
    print("\nKey visualizations for report:")
    print("  📊 Gantt charts: *_gantt.png")
    print("  📈 Performance: makespan_comparison_detailed.png")
    print("  📊 Success rates: success_rate_stacked_bar.png")
    print("  🔥 Summary: algorithm_summary_heatmap.png")
    print("  📉 DPE analysis: deadline_pressure_*.png")
    print("\nThese are publication-quality (300 DPI) and ready for:")
    print("  • LaTeX \\includegraphics{}")
    print("  • Word document insertion")
    print("  • Poster design software")
    print("=" * 70)


def create_poster_specific_figures():
    """Generate figures specifically optimized for poster presentation"""
    print("\n" + "=" * 70)
    print("GENERATING POSTER-SPECIFIC FIGURES")
    print("=" * 70)
    print("\nPoster figures should be:")
    print("  • Larger font sizes (14-16pt)")
    print("  • High contrast colors")
    print("  • Minimal text")
    print("  • Clear visual hierarchy")
    print("\n⚠️ TODO: Customize sizing for poster format")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    import numpy as np

    if len(sys.argv) > 1 and sys.argv[1] == "--poster":
        create_poster_specific_figures()
    else:
        create_comprehensive_report_figures()
