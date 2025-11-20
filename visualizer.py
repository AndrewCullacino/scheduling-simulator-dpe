"""
Visualization System for COMP3821 Scheduling Project
=====================================================

Comprehensive publication-quality visualizations including:
1. Gantt charts showing task scheduling timelines
2. Algorithm performance comparisons
3. Alpha sensitivity analysis
4. Performance heatmaps
5. Success rate analysis by priority
6. Pareto frontier analysis

All outputs optimized for academic publication (300 DPI).

Author: Group 5
Date: November 2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import os
import copy
from simple_simulator import Task, Priority
from algorithms import get_all_algorithms
from scenarios import get_all_scenarios

# =============================================================================
# MATPLOTLIB CONFIGURATION
# =============================================================================

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

sns.set_style("whitegrid", {'grid.linestyle': '--', 'grid.alpha': 0.3})

# Colorblind-friendly palette
ALGORITHM_COLORS = {
    'SPT': '#E69F00',
    'EDF': '#56B4E9',
    'Priority-First': '#009E73',
    'DPE (α=0.3)': '#0072B2',
    'DPE (α=0.5)': '#CC79A7',
    'DPE (α=0.7)': '#D55E00',
    'DPE (α=0.9)': '#F0E442'
}

PRIORITY_COLORS = {
    'high_priority': '#2E86AB',
    'low_priority': '#F77F00',
    'deadline_missed': '#D62828'
}


# =============================================================================
# SCHEDULING VISUALIZER CLASS
# =============================================================================

class SchedulingVisualizer:
    """Visualization system for scheduling analysis"""

    def __init__(self, output_dir='visualizations'):
        """Initialize visualizer with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def create_gantt_chart(self, tasks, algorithm_name, scenario_name,
                          num_machines=2, save=True):
        """
        Create Gantt chart showing task scheduling timeline.

        Args:
            tasks: List of Task objects with scheduling information
            algorithm_name: Name of algorithm for title
            scenario_name: Name of scenario for title
            num_machines: Number of machines to display
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, max(3, num_machines * 0.8)))

        # Plot each task as a rectangle
        for task in tasks:
            if task.start_time is None or task.completion_time is None:
                continue

            # Determine color based on priority and deadline status
            if task.meets_deadline():
                color = PRIORITY_COLORS['high_priority'] if task.priority.name == 'HIGH' else PRIORITY_COLORS['low_priority']
                alpha = 0.8
                edge_color = 'black'
                edge_width = 1
            else:
                # Deadline missed - use red border
                color = PRIORITY_COLORS['high_priority'] if task.priority.name == 'HIGH' else PRIORITY_COLORS['low_priority']
                alpha = 0.5
                edge_color = PRIORITY_COLORS['deadline_missed']
                edge_width = 3

            # Draw task rectangle
            machine_y = task.machine_id
            duration = task.completion_time - task.start_time

            rect = Rectangle(
                (task.start_time, machine_y - 0.4),
                duration, 0.8,
                facecolor=color,
                edgecolor=edge_color,
                linewidth=edge_width,
                alpha=alpha
            )
            ax.add_patch(rect)

            # Add task ID label
            task_label = f"T{task.id}"
            ax.text(
                task.start_time + duration/2,
                machine_y,
                task_label,
                ha='center', va='center',
                fontsize=9,
                fontweight='bold',
                color='white'
            )

            # Draw deadline marker (vertical dashed line)
            ax.plot([task.deadline, task.deadline],
                   [machine_y - 0.45, machine_y + 0.45],
                   color='gray', linestyle=':', linewidth=1.5, alpha=0.6)

        # Configure axes
        ax.set_xlim(0, max((t.completion_time for t in tasks if t.completion_time), default=10) + 2)
        ax.set_ylim(-0.5, num_machines - 0.5)
        ax.set_xlabel('Time', fontsize=11, fontweight='bold')
        ax.set_ylabel('Machine', fontsize=11, fontweight='bold')
        ax.set_title(f'{algorithm_name} - {scenario_name}', fontsize=13, fontweight='bold', pad=15)
        ax.set_yticks(range(num_machines))
        ax.set_yticklabels([f'M{i}' for i in range(num_machines)])
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.invert_yaxis()

        # Create legend
        legend_elements = [
            mpatches.Patch(facecolor=PRIORITY_COLORS['high_priority'], edgecolor='black', label='High Priority'),
            mpatches.Patch(facecolor=PRIORITY_COLORS['low_priority'], edgecolor='black', label='Low Priority'),
            mpatches.Patch(facecolor='white', edgecolor=PRIORITY_COLORS['deadline_missed'], linewidth=3, label='Deadline Missed')
        ]
        ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

        plt.tight_layout()

        if save:
            safe_algo = algorithm_name.replace('(', '').replace(')', '').replace(' ', '_').replace('=', '')
            safe_scenario = scenario_name.replace(' ', '_').replace(':', '').replace('/', '_')
            filename = f"{safe_scenario}_{safe_algo}_gantt.png"
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close(fig)

        return fig


# =============================================================================
# AGGREGATE VISUALIZATION FUNCTIONS
# =============================================================================

def load_results_data(csv_path='results/comprehensive_results.csv'):
    """Load experimental results from CSV"""
    csv_path = Path(csv_path)
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(df)} experimental results")
        return df
    else:
        print(f"❌ File not found: {csv_path}")
        return None


def categorize_scenario(scenario_name):
    """Categorize scenarios by type"""
    if any(x in scenario_name for x in ['Light', 'Heavy', 'Batch', 'Starvation Test']):
        return 'Basic'
    elif 'Challenge' in scenario_name:
        return 'Challenge'
    elif 'Extreme' in scenario_name:
        return 'Extreme'
    elif 'Advanced' in scenario_name:
        return 'Advanced'
    elif 'New' in scenario_name:
        return 'New'
    return 'Other'


def create_algorithm_performance_by_category(df, output_dir='visualizations'):
    """
    Algorithm performance comparison across scenario categories.
    Grouped bar chart showing mean composite performance scores.
    """
    print("\n📊 Generating Algorithm Performance Comparison...")

    df['Category'] = df['Scenario'].apply(categorize_scenario)
    perf_data = df.groupby(['Algorithm', 'Category'])['Composite Performance Score (%)'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 8))

    categories = ['Basic', 'Challenge', 'Extreme', 'Advanced', 'New']
    algorithms = df['Algorithm'].unique()

    x = np.arange(len(categories))
    width = 0.12
    multiplier = 0

    for algorithm in algorithms:
        alg_data = perf_data[perf_data['Algorithm'] == algorithm]
        values = [alg_data[alg_data['Category'] == cat]['Composite Performance Score (%)'].values[0]
                  if len(alg_data[alg_data['Category'] == cat]) > 0 else 0
                  for cat in categories]

        offset = width * multiplier
        bars = ax.bar(x + offset, values, width,
                     label=algorithm,
                     color=ALGORITHM_COLORS.get(algorithm, '#999999'),
                     edgecolor='black', linewidth=0.5)

        for i, (bar, val) in enumerate(zip(bars, values)):
            if val > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{val:.1f}',
                       ha='center', va='bottom', fontsize=7)

        multiplier += 1

    ax.set_xlabel('Scenario Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Composite Performance Score (%)', fontsize=12, fontweight='bold')
    ax.set_title('Algorithm Performance Across Scenario Categories\n(Balancing Success Rate & Makespan Efficiency)',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x + width * 3)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 110)
    ax.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.legend(loc='lower left', ncol=2, framealpha=0.95)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    output_path = Path(output_dir) / 'algorithm_performance_by_category.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {output_path}")


def create_alpha_sensitivity_clean(df, output_dir='visualizations'):
    """
    DPE alpha sensitivity analysis showing threshold effect on low-priority success rates.
    """
    print("\n📊 Generating Alpha Sensitivity Analysis...")

    dpe_data = df[df['Algorithm'].str.contains('DPE')].copy()
    dpe_data['Alpha'] = dpe_data['Algorithm'].str.extract(r'α=(\d\.\d)')[0].astype(float)
    dpe_data['Category'] = dpe_data['Scenario'].apply(categorize_scenario)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Panel 1: By Category
    categories = ['Basic', 'Challenge', 'Extreme', 'Advanced', 'New']
    colors_cat = ['#2E86AB', '#E63946', '#F77F00', '#7209B7', '#06A77D']

    for category, color in zip(categories, colors_cat):
        cat_data = dpe_data[dpe_data['Category'] == category].groupby('Alpha')['Low Success Rate (%)'].mean()
        if len(cat_data) > 0:
            ax1.plot(cat_data.index, cat_data.values, marker='o', markersize=8,
                    linewidth=2.5, label=category, color=color)

    ax1.axvspan(0.25, 0.5, alpha=0.1, color='green', label='Optimal Range')
    ax1.axvline(x=0.5, color='#2A9D8F', linestyle='--', linewidth=2, label='Critical Threshold')
    ax1.set_xlabel('Alpha Parameter (α)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Low-Priority Success Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Alpha Sensitivity by Scenario Category', fontsize=13, fontweight='bold')
    ax1.set_xlim(0.25, 0.95)
    ax1.set_ylim(0, 105)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='lower left', fontsize=9)

    # Panel 2: Overall Trend
    overall = dpe_data.groupby('Alpha')['Low Success Rate (%)'].agg(['mean', 'std']).reset_index()
    ax2.plot(overall['Alpha'], overall['mean'], marker='o', markersize=10,
            linewidth=3, color='#2E86AB', label='Mean')
    ax2.fill_between(overall['Alpha'],
                     overall['mean'] - overall['std'],
                     overall['mean'] + overall['std'],
                     alpha=0.2, color='#2E86AB')
    ax2.axvspan(0.25, 0.5, alpha=0.1, color='green')
    ax2.axvline(x=0.5, color='#2A9D8F', linestyle='--', linewidth=2)
    ax2.annotate('Optimal (α ≤ 0.5)', xy=(0.4, 90), fontsize=10, color='#2A9D8F',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#2A9D8F'))
    ax2.set_xlabel('Alpha Parameter (α)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Low-Priority Success Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Overall Alpha Sensitivity', fontsize=13, fontweight='bold')
    ax2.set_xlim(0.25, 0.95)
    ax2.set_ylim(0, 105)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = Path(output_dir) / 'alpha_sensitivity_clean.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {output_path}")


def create_performance_heatmap_clean(df, output_dir='visualizations'):
    """
    Performance heatmap showing composite performance scores (Scenario × Algorithm).
    """
    print("\n📊 Generating Performance Heatmap...")

    pivot_data = df.pivot_table(
        values='Composite Performance Score (%)',
        index='Scenario',
        columns='Algorithm',
        aggfunc='mean'
    )

    algorithm_order = ['SPT', 'EDF', 'Priority-First', 'DPE (α=0.3)', 'DPE (α=0.5)', 'DPE (α=0.7)', 'DPE (α=0.9)']
    pivot_data = pivot_data[algorithm_order]

    fig, ax = plt.subplots(figsize=(14, 16))

    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn',
                vmin=0, vmax=100, center=70, linewidths=0.5,
                cbar_kws={'label': 'Composite Performance Score (%)'}, ax=ax)

    ax.set_title('Algorithm Performance Heatmap\nComposite Scores (Success Rate + Makespan Efficiency) Across All Scenarios',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Scenario', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    output_path = Path(output_dir) / 'performance_heatmap_clean.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {output_path}")


def create_success_rate_by_priority(df, output_dir='visualizations'):
    """
    Success rate comparison for high vs low priority tasks by algorithm.
    """
    print("\n📊 Generating Success Rate by Priority...")

    priority_data = df.groupby('Algorithm').agg({
        'High Success Rate (%)': 'mean',
        'Low Success Rate (%)': 'mean'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(priority_data))
    width = 0.35

    bars1 = ax.bar(x - width/2, priority_data['High Success Rate (%)'], width,
                   label='High Priority', color='#2E86AB', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, priority_data['Low Success Rate (%)'], width,
                   label='Low Priority', color='#F77F00', edgecolor='black', linewidth=0.5)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Success Rates by Priority Class\nComparison Across Algorithms',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(priority_data['Algorithm'], rotation=45, ha='right')
    ax.set_ylim(0, 110)
    ax.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.legend(fontsize=11)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    output_path = Path(output_dir) / 'success_rate_by_priority.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {output_path}")


def create_pareto_frontier_clean(df, output_dir='visualizations'):
    """
    Pareto frontier analysis: Fairness vs Efficiency trade-off.
    """
    print("\n📊 Generating Pareto Frontier...")

    pareto_data = df.groupby('Algorithm').agg({
        'High Success Rate (%)': 'mean',
        'Low Success Rate (%)': 'mean',
        'Makespan': 'mean'
    }).reset_index()

    pareto_data['Fairness'] = pareto_data['Low Success Rate (%)']
    pareto_data['Efficiency'] = pareto_data['High Success Rate (%)']

    fig, ax = plt.subplots(figsize=(12, 8))

    for _, row in pareto_data.iterrows():
        ax.scatter(row['Fairness'], row['Efficiency'],
                  s=200, alpha=0.7,
                  color=ALGORITHM_COLORS.get(row['Algorithm'], '#999999'),
                  edgecolors='black', linewidths=1.5,
                  label=row['Algorithm'])

        ax.annotate(row['Algorithm'],
                   (row['Fairness'], row['Efficiency']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=9, fontweight='bold')

    ax.set_xlabel('Fairness (Low-Priority Success Rate %)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Efficiency (High-Priority Success Rate %)', fontsize=12, fontweight='bold')
    ax.set_title('Pareto Frontier: Fairness vs Efficiency Trade-off',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(-5, 105)
    ax.set_ylim(85, 105)
    ax.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=70, color='orange', linestyle=':', linewidth=1.5, alpha=0.5,
              label='Fairness Threshold (70%)')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = Path(output_dir) / 'pareto_frontier_clean.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: {output_path}")


def generate_all_gantt_charts(output_dir='visualizations'):
    """
    Generate Gantt charts for all scenarios and algorithms.
    Total: 24 scenarios × 7 algorithms = 168 charts
    """
    print("\n" + "=" * 80)
    print("GENERATING ALL GANTT CHARTS")
    print("=" * 80)

    viz = SchedulingVisualizer(output_dir=output_dir)
    scenarios = get_all_scenarios()
    algorithms_dict = get_all_algorithms()

    algorithms = [
        ("SPT", algorithms_dict['SPT']),
        ("EDF", algorithms_dict['EDF']),
        ("Priority-First", algorithms_dict['Priority-First']),
        ("DPE (α=0.3)", algorithms_dict['DPE (α=0.3)']),
        ("DPE (α=0.5)", algorithms_dict['DPE (α=0.5)']),
        ("DPE (α=0.7)", algorithms_dict['DPE (α=0.7)']),
        ("DPE (α=0.9)", algorithms_dict['DPE (α=0.9)']),
    ]

    total_charts = 0

    for i, scenario in enumerate(scenarios, 1):
        scenario_name = scenario['name']
        print(f"\n{i}. {scenario_name}")

        for algo_name, SchedulerClass in algorithms:
            tasks_copy = copy.deepcopy(scenario['tasks'])
            scheduler = SchedulerClass(tasks_copy, scenario['num_machines'])
            scheduler.run()

            viz.create_gantt_chart(
                tasks_copy,
                algo_name,
                scenario_name,
                num_machines=scenario['num_machines'],
                save=True
            )
            total_charts += 1

        print(f"   ✅ Generated 7 charts")

    print(f"\n✅ Total Gantt charts generated: {total_charts}")


def generate_all_aggregate_visualizations(csv_path='results/comprehensive_results.csv',
                                          output_dir='visualizations'):
    """
    Generate all aggregate analysis visualizations from experimental results.
    """
    print("\n" + "=" * 80)
    print("GENERATING AGGREGATE VISUALIZATIONS")
    print("=" * 80)

    df = load_results_data(csv_path)
    if df is None:
        return

    create_algorithm_performance_by_category(df, output_dir)
    create_alpha_sensitivity_clean(df, output_dir)
    create_performance_heatmap_clean(df, output_dir)
    create_success_rate_by_priority(df, output_dir)
    create_pareto_frontier_clean(df, output_dir)

    print("\n✅ All aggregate visualizations generated!")


if __name__ == "__main__":
    print("=" * 80)
    print("VISUALIZATION SYSTEM")
    print("=" * 80)
    print("\n1. Generate all Gantt charts (168 total)")
    print("2. Generate all aggregate visualizations (5 charts)")
    print("\nStarting generation...")

    generate_all_gantt_charts()
    generate_all_aggregate_visualizations()

    print("\n" + "=" * 80)
    print("✅ ALL VISUALIZATIONS COMPLETE!")
    print("=" * 80)
    print(f"\nOutput directory: visualizations/")
    print(f"Total files: 173 PNG files")
    print("  • 168 Gantt charts (24 scenarios × 7 algorithms)")
    print("  • 5 aggregate analysis charts")
    print("=" * 80)
