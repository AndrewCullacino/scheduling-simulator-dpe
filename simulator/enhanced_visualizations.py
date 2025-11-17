"""
Enhanced Visualization System for COMP3821 Scheduling Project
==============================================================

Publication-quality visualizations for final report and poster presentation.

Features:
1. Gantt charts showing task scheduling timelines
2. Performance comparison charts (makespan, success rates)
3. Deadline pressure heatmaps for DPE analysis
4. Statistical distribution plots
5. Scenario complexity analysis

All outputs optimized for academic publication (300 DPI, proper sizing).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List, Dict, Tuple
import os

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Color scheme for consistency
COLORS = {
    'high_priority': '#2E86AB',  # Blue
    'low_priority': '#F77F00',   # Orange
    'deadline_met': '#06A77D',   # Green
    'deadline_missed': '#D62828', # Red
    'spt': '#4ECDC4',
    'edf': '#FF6B6B',
    'priority_first': '#95E1D3',
    'dpe': '#F38181',
    'dpe_0.5': '#FF8FA3',  # Pink for DPE α=0.5
    'dpe_0.7': '#F38181',  # Original DPE color for α=0.7
    'dpe_0.9': '#C54040'   # Darker red for DPE α=0.9
}


class SchedulingVisualizer:
    """Enhanced visualization system for scheduling analysis"""

    def __init__(self, output_dir='visualizations'):
        """Initialize visualizer with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_gantt_chart(self, tasks, algorithm_name, scenario_name,
                          num_machines=2, save=True):
        """
        Create Gantt chart showing task scheduling timeline.

        Args:
            tasks: List of Task objects with start_time, completion_time, etc.
            algorithm_name: Name of the algorithm (for title)
            scenario_name: Name of the scenario (for title)
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
                if task.priority.name == 'HIGH':
                    color = COLORS['high_priority']
                    alpha = 0.8
                else:
                    color = COLORS['low_priority']
                    alpha = 0.8
                edge_color = 'black'
                edge_width = 1
            else:
                # Deadline missed - use red border
                if task.priority.name == 'HIGH':
                    color = COLORS['high_priority']
                else:
                    color = COLORS['low_priority']
                alpha = 0.5
                edge_color = COLORS['deadline_missed']
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
                fontsize=8, fontweight='bold',
                color='white' if alpha > 0.5 else 'black'
            )

            # Draw deadline marker (vertical dashed line)
            ax.axvline(
                task.deadline,
                ymin=(machine_y - 0.5) / num_machines,
                ymax=(machine_y + 0.5) / num_machines,
                color='gray',
                linestyle='--',
                alpha=0.5,
                linewidth=1
            )

        # Styling
        ax.set_xlabel('Time', fontweight='bold')
        ax.set_ylabel('Machine', fontweight='bold')
        ax.set_title(f'{algorithm_name} - {scenario_name}',
                    fontweight='bold', pad=15)

        # Set y-axis ticks for machines
        ax.set_yticks(range(num_machines))
        ax.set_yticklabels([f'M{i}' for i in range(num_machines)])

        # Set x-axis limits
        if tasks:
            max_time = max(t.completion_time for t in tasks if t.completion_time)
            ax.set_xlim(0, max_time * 1.1)

        ax.set_ylim(-0.5, num_machines - 0.5)
        ax.grid(True, axis='x', alpha=0.3, linestyle=':')

        # Legend
        high_patch = mpatches.Patch(color=COLORS['high_priority'],
                                    label='High Priority', alpha=0.8)
        low_patch = mpatches.Patch(color=COLORS['low_priority'],
                                   label='Low Priority', alpha=0.8)
        missed_patch = mpatches.Patch(edgecolor=COLORS['deadline_missed'],
                                     facecolor='white', linewidth=3,
                                     label='Deadline Missed')
        deadline_line = mpatches.Patch(color='gray', label='Deadline',
                                      linestyle='--', alpha=0.5)

        ax.legend(handles=[high_patch, low_patch, missed_patch],
                 loc='upper right', framealpha=0.9)

        plt.tight_layout()

        if save:
            filename = f"{scenario_name.replace(' ', '_')}_{algorithm_name.replace(' ', '_')}_gantt.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved Gantt chart: {filepath}")

        return fig

    def create_performance_comparison(self, results_df, metric='makespan', save=True):
        """
        Create bar chart comparing algorithm performance across scenarios.

        Args:
            results_df: pandas DataFrame with columns: Scenario, Algorithm, metric
            metric: Metric to compare ('makespan', 'success_rate', etc.)
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        # Prepare data
        scenarios = results_df['Scenario'].unique()
        algorithms = results_df['Algorithm'].unique()

        x = np.arange(len(scenarios))
        width = 0.2

        # Plot bars for each algorithm
        for i, algo in enumerate(algorithms):
            algo_data = results_df[results_df['Algorithm'] == algo]
            values = [algo_data[algo_data['Scenario'] == s][metric].values[0]
                     if len(algo_data[algo_data['Scenario'] == s]) > 0 else 0
                     for s in scenarios]

            offset = width * (i - len(algorithms)/2 + 0.5)
            bars = ax.bar(x + offset, values, width, label=algo, alpha=0.8)

        # Styling
        ax.set_xlabel('Scenario', fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title(), fontweight='bold')
        ax.set_title(f'{metric.replace("_", " ").title()} Comparison Across Scenarios',
                    fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios, rotation=45, ha='right')
        ax.legend(title='Algorithm', loc='upper left', framealpha=0.9)
        ax.grid(True, axis='y', alpha=0.3, linestyle=':')

        plt.tight_layout()

        if save:
            filename = f"performance_comparison_{metric}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved performance comparison: {filepath}")

        return fig

    def create_success_rate_stacked_bar(self, results_df, save=True):
        """
        Create stacked bar chart showing high/low priority success rates.

        Args:
            results_df: pandas DataFrame with success rate data
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        scenarios = results_df['Scenario'].unique()
        algorithms = results_df['Algorithm'].unique()

        x = np.arange(len(scenarios))
        width = 0.2

        for i, algo in enumerate(algorithms):
            algo_data = results_df[results_df['Algorithm'] == algo]

            high_success = []
            low_success = []

            for s in scenarios:
                scenario_data = algo_data[algo_data['Scenario'] == s]
                if len(scenario_data) > 0:
                    high_success.append(scenario_data['High Success Rate'].values[0])
                    low_success.append(scenario_data['Low Success Rate'].values[0])
                else:
                    high_success.append(0)
                    low_success.append(0)

            offset = width * (i - len(algorithms)/2 + 0.5)

            # Stack high priority (bottom) and low priority (top)
            ax.bar(x + offset, high_success, width,
                  label=f'{algo} (High Priority)' if i == 0 else "",
                  color=COLORS['high_priority'], alpha=0.8)
            ax.bar(x + offset, low_success, width, bottom=high_success,
                  label=f'{algo} (Low Priority)' if i == 0 else "",
                  color=COLORS['low_priority'], alpha=0.8)

        # Styling
        ax.set_xlabel('Scenario', fontweight='bold')
        ax.set_ylabel('Success Rate (%)', fontweight='bold')
        ax.set_title('Deadline Success Rates by Priority Class',
                    fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios, rotation=45, ha='right')
        ax.set_ylim(0, 105)
        ax.axhline(y=100, color='green', linestyle='--', alpha=0.3, linewidth=1)
        ax.legend(loc='upper right', framealpha=0.9)
        ax.grid(True, axis='y', alpha=0.3, linestyle=':')

        plt.tight_layout()

        if save:
            filename = "success_rate_stacked_bar.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved success rate chart: {filepath}")

        return fig

    def create_deadline_pressure_plot(self, tasks, alpha_threshold=0.7, save=True):
        """
        Create line plot showing deadline pressure evolution over time.

        Args:
            tasks: List of Task objects
            alpha_threshold: DPE threshold to visualize
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Calculate pressure over time for each task
        max_time = max(t.completion_time for t in tasks if t.completion_time)
        time_points = np.linspace(0, max_time, 100)

        for task in tasks:
            if task.priority.name == 'LOW':  # Only show low priority tasks
                pressures = []
                for t in time_points:
                    if t >= task.arrival_time:
                        if task.start_time and t >= task.start_time:
                            # Task already started, pressure stops
                            pressures.append(None)
                        else:
                            # Calculate pressure
                            elapsed = t - task.arrival_time
                            available = task.deadline - task.arrival_time
                            pressure = elapsed / available if available > 0 else 1.0
                            pressures.append(min(pressure, 1.0))
                    else:
                        pressures.append(None)

                # Plot task pressure line
                ax.plot(time_points, pressures, label=f'Task {task.id}',
                       linewidth=2, alpha=0.7)

                # Mark when task starts (circle marker)
                if task.start_time:
                    start_pressure = (task.start_time - task.arrival_time) / \
                                   (task.deadline - task.arrival_time)
                    ax.scatter([task.start_time], [start_pressure],
                             s=100, marker='o', zorder=5)

        # Draw alpha threshold line
        ax.axhline(y=alpha_threshold, color='red', linestyle='--',
                  linewidth=2, label=f'α = {alpha_threshold} (Elevation Threshold)')

        # Styling
        ax.set_xlabel('Time', fontweight='bold')
        ax.set_ylabel('Deadline Pressure', fontweight='bold')
        ax.set_title('Low-Priority Task Deadline Pressure Evolution',
                    fontweight='bold', pad=15)
        ax.set_ylim(0, 1.05)
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle=':')

        # Add annotation for elevation zone
        ax.fill_between([0, max_time], alpha_threshold, 1.0,
                       color='red', alpha=0.1, label='Elevation Zone')

        plt.tight_layout()

        if save:
            filename = f"deadline_pressure_alpha{alpha_threshold}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved deadline pressure plot: {filepath}")

        return fig

    def create_algorithm_summary_heatmap(self, results_df, save=True):
        """
        Create heatmap showing algorithm success rates across all scenarios.

        Args:
            results_df: pandas DataFrame with success rate data
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # Pivot data for heatmap
        pivot_data = results_df.pivot(index='Scenario',
                                      columns='Algorithm',
                                      values='Total Success Rate')

        # Create heatmap
        sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn',
                   vmin=0, vmax=100, cbar_kws={'label': 'Success Rate (%)'},
                   linewidths=0.5, linecolor='gray', ax=ax)

        # Styling
        ax.set_title('Algorithm Success Rates Across All Scenarios',
                    fontweight='bold', pad=15)
        ax.set_xlabel('Algorithm', fontweight='bold')
        ax.set_ylabel('Scenario', fontweight='bold')

        plt.tight_layout()

        if save:
            filename = "algorithm_summary_heatmap.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved summary heatmap: {filepath}")

        return fig

    def create_response_time_boxplot(self, all_results, save=True):
        """
        Create box plot comparing response time distributions.

        Args:
            all_results: Dict mapping algorithm names to lists of tasks
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Prepare data
        data = []
        labels = []

        for algo_name, tasks in all_results.items():
            response_times = [t.completion_time - t.arrival_time
                            for t in tasks if t.completion_time]
            data.append(response_times)
            labels.append(algo_name)

        # Create box plot
        bp = ax.boxplot(data, labels=labels, patch_artist=True,
                       showmeans=True, meanline=True)

        # Color boxes
        colors = [COLORS['spt'], COLORS['edf'], COLORS['priority_first'], COLORS['dpe']]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Styling
        ax.set_xlabel('Algorithm', fontweight='bold')
        ax.set_ylabel('Response Time', fontweight='bold')
        ax.set_title('Response Time Distribution Comparison',
                    fontweight='bold', pad=15)
        ax.grid(True, axis='y', alpha=0.3, linestyle=':')

        plt.tight_layout()

        if save:
            filename = "response_time_boxplot.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved box plot: {filepath}")

        return fig

    def create_makespan_comparison_detailed(self, results_df, save=True):
        """
        Create detailed makespan comparison with error indicators.

        Args:
            results_df: pandas DataFrame with makespan data
            save: Whether to save the figure

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(18, 7))

        scenarios = results_df['Scenario'].unique()
        algorithms = results_df['Algorithm'].unique()

        x = np.arange(len(scenarios))
        width = 0.14

        # Find minimum makespan per scenario for comparison
        min_makespans = []
        for s in scenarios:
            scenario_data = results_df[results_df['Scenario'] == s]
            min_makespans.append(scenario_data['Makespan'].min())

        # Plot bars for each algorithm - dynamically map colors
        def get_algo_color(algo_name):
            """Map algorithm name to color"""
            algo_lower = algo_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('α=', '')
            if 'spt' in algo_lower:
                return COLORS['spt']
            elif 'edf' in algo_lower:
                return COLORS['edf']
            elif 'priority' in algo_lower:
                return COLORS['priority_first']
            elif 'dpe' in algo_lower:
                if '0.5' in algo_name:
                    return COLORS['dpe_0.5']
                elif '0.9' in algo_name:
                    return COLORS['dpe_0.9']
                else:
                    return COLORS['dpe_0.7']
            else:
                return '#808080'  # Gray for unknown

        for i, algo in enumerate(algorithms):
            algo_data = results_df[results_df['Algorithm'] == algo]
            makespans = []

            for s in scenarios:
                scenario_data = algo_data[algo_data['Scenario'] == s]
                if len(scenario_data) > 0:
                    makespans.append(scenario_data['Makespan'].values[0])
                else:
                    makespans.append(0)

            offset = width * (i - len(algorithms)/2 + 0.5)

            # Get color for this algorithm
            algo_color = get_algo_color(algo)

            # Highlight bars that match minimum (optimal)
            colors = [algo_color if m == min_m else algo_color
                     for m, min_m in zip(makespans, min_makespans)]
            alphas = [1.0 if m == min_m else 0.6
                     for m, min_m in zip(makespans, min_makespans)]

            bars = ax.bar(x + offset, makespans, width, label=algo,
                         color=colors, alpha=alphas[0], edgecolor='black',
                         linewidth=0.5)

            # Add value labels on top of bars
            for bar, val in zip(bars, makespans):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, val + 0.2,
                           f'{val:.0f}', ha='center', va='bottom',
                           fontsize=5)

        # Styling
        ax.set_xlabel('Scenario', fontweight='bold')
        ax.set_ylabel('Makespan (time units)', fontweight='bold')
        ax.set_title('Makespan Comparison Across Scenarios (optimal = best)',
                    fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios, rotation=45, ha='right')
        ax.legend(title='Algorithm', loc='upper left', framealpha=0.9, ncol=2)
        ax.grid(True, axis='y', alpha=0.3, linestyle=':')

        # Add horizontal line at 0
        ax.axhline(y=0, color='black', linewidth=0.8)

        plt.tight_layout()

        if save:
            filename = "makespan_comparison_detailed.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✅ Saved detailed makespan comparison: {filepath}")

        return fig


def demo_visualizations():
    """Demonstrate visualization system with sample data"""
    from simple_simulator import Task, Priority

    print("=" * 70)
    print("DEMONSTRATION: Enhanced Visualization System")
    print("=" * 70)

    # Create sample tasks
    tasks = [
        Task(1, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=10),
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=12),
        Task(3, arrival_time=1, processing_time=4, priority=Priority.LOW, deadline=25),
        Task(4, arrival_time=2, processing_time=5, priority=Priority.LOW, deadline=30),
    ]

    # Simulate scheduling (set start/completion times)
    tasks[0].start_time = 0
    tasks[0].completion_time = 3
    tasks[0].machine_id = 0

    tasks[1].start_time = 0
    tasks[1].completion_time = 2
    tasks[1].machine_id = 1

    tasks[2].start_time = 2
    tasks[2].completion_time = 6
    tasks[2].machine_id = 1

    tasks[3].start_time = 3
    tasks[3].completion_time = 8
    tasks[3].machine_id = 0

    # Create visualizer
    viz = SchedulingVisualizer(output_dir='demo_visualizations')

    # Generate visualizations
    print("\n1. Creating Gantt chart...")
    viz.create_gantt_chart(tasks, "SPT Algorithm", "Demo Scenario", num_machines=2)

    print("\n2. Creating deadline pressure plot...")
    viz.create_deadline_pressure_plot(tasks, alpha_threshold=0.7)

    print("\n✨ Demonstration complete! Check 'demo_visualizations/' directory")
    print("=" * 70)


if __name__ == "__main__":
    demo_visualizations()
