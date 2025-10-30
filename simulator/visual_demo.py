"""
Simple Visual Demonstration of Algorithm Differences
====================================================

This shows EXACTLY when and how algorithms differ.
"""

from simple_simulator import (
    Task, Priority,
    SPT_Scheduler, EDF_Scheduler,
    PriorityFirst_Scheduler, DPE_Scheduler
)
import copy
import csv
import os


def demo_case_1():
    """
    DEMONSTRATION: SPT vs EDF
    
    Setup:
    - Task A: short (2 units), loose deadline (50)
    - Task B: long (10 units), TIGHT deadline (11)
    
    SPT will do: A then B → B completes at 12 → MISSES deadline 11!
    EDF will do: B then A → B completes at 10 → MEETS deadline 11!
    """
    print("\n" + "=" * 80)
    print("DEMO 1: SPT vs EDF - Deadline Awareness")
    print("=" * 80)
    print("\nSetup:")
    print("  Task A: processing=2, deadline=50")
    print("  Task B: processing=10, deadline=11  ← TIGHT!")
    print("  1 machine\n")
    
    tasks = [
        Task('A', 0, 2, Priority.HIGH, 50),
        Task('B', 0, 10, Priority.HIGH, 11),
    ]
    
    print("SPT Strategy (shortest first):")
    print("  Time 0-2: Run A (short)")
    print("  Time 2-12: Run B")
    print("  Result: B completes at 12 > deadline 11  ❌ MISS!")
    
    spt_tasks = copy.deepcopy(tasks)
    spt = SPT_Scheduler(spt_tasks, 1)
    spt.run()
    
    task_b_spt = [t for t in spt_tasks if t.id == 'B'][0]
    print(f"  Actual: B completes at {task_b_spt.completion_time}, deadline {task_b_spt.deadline}")
    print(f"  Status: {'✅ MET' if task_b_spt.meets_deadline() else '❌ MISSED'}")
    
    print("\nEDF Strategy (earliest deadline first):")
    print("  Time 0-10: Run B (tight deadline)")
    print("  Time 10-12: Run A")
    print("  Result: B completes at 10 < deadline 11  ✅ MET!")
    
    edf_tasks = copy.deepcopy(tasks)
    edf = EDF_Scheduler(edf_tasks, 1)
    edf.run()
    
    task_b_edf = [t for t in edf_tasks if t.id == 'B'][0]
    print(f"  Actual: B completes at {task_b_edf.completion_time}, deadline {task_b_edf.deadline}")
    print(f"  Status: {'✅ MET' if task_b_edf.meets_deadline() else '❌ MISSED'}")

    # Export results for demo_case_1
    export_run_results('demo1_SPT', spt_tasks)
    export_run_results('demo1_EDF', edf_tasks)


def demo_case_2():
    """
    DEMONSTRATION: Priority-First vs DPE - Starvation
    
    Setup:
    - Low-priority task L: processing=5, deadline=17
    - High-priority tasks H1, H2, H3: each processing=4
    - 1 machine
    
    Priority-First will do: H1, H2, H3, then L
    → L starts at time 12, completes at 17 → barely makes it or misses!
    
    DPE will: Start H1, but elevate L before it's too late
    """
    print("\n" + "=" * 80)
    print("DEMO 2: Priority-First vs DPE - Preventing Starvation")
    print("=" * 80)
    print("\nSetup:")
    print("  Task L: LOW priority, processing=5, deadline=17")
    print("  Tasks H1, H2, H3: HIGH priority, each processing=4, loose deadlines")
    print("  1 machine\n")
    
    tasks = [
        Task('L', 0, 5, Priority.LOW, 17),  # Low priority, deadline 17
        Task('H1', 0, 4, Priority.HIGH, 30),
        Task('H2', 4, 4, Priority.HIGH, 35),
        Task('H3', 8, 4, Priority.HIGH, 40),
    ]
    
    print("Priority-First Strategy:")
    print("  Always does HIGH priority first")
    print("  Time 0-4: H1")
    print("  Time 4-8: H2")
    print("  Time 8-12: H3")
    print("  Time 12-17: L  ← just barely makes deadline 17")
    
    pf_tasks = copy.deepcopy(tasks)
    pf = PriorityFirst_Scheduler(pf_tasks, 1)
    pf.run()
    
    task_l_pf = [t for t in pf_tasks if t.id == 'L'][0]
    print(f"  Actual: L completes at {task_l_pf.completion_time}, deadline {task_l_pf.deadline}")
    print(f"  Status: {'✅ MET' if task_l_pf.meets_deadline() else '❌ MISSED'}")
    
    print("\nDPE Strategy (α=0.7):")
    print("  Monitors deadline pressure for L")
    print("  L's deadline window: 17-0 = 17")
    print("  At time 11.9: pressure = 11.9/17 = 0.70 → ELEVATE L!")
    print("  Time 0-4: H1")
    print("  Time 4-8: H2")
    print("  Time 8-13: L (elevated before H3!) ✅")
    print("  Time 13-17: H3")
    
    dpe_tasks = copy.deepcopy(tasks)
    dpe = DPE_Scheduler(dpe_tasks, 1, alpha=0.7)
    dpe.run()
    
    task_l_dpe = [t for t in dpe_tasks if t.id == 'L'][0]
    print(f"  Actual: L completes at {task_l_dpe.completion_time}, deadline {task_l_dpe.deadline}")
    print(f"  Status: {'✅ MET' if task_l_dpe.meets_deadline() else '❌ MISSED'}")

    # Export results for demo_case_2
    export_run_results('demo2_PriorityFirst', pf_tasks)
    export_run_results('demo2_DPE_a0.7', dpe_tasks)


def demo_case_3():
    """
    DEMONSTRATION: Different α values produce different results
    """
    print("\n" + "=" * 80)
    print("DEMO 3: DPE with Different α Values")
    print("=" * 80)
    print("\nSetup:")
    print("  Task L: LOW priority, processing=4, deadline=20")
    print("  Tasks H1-H5: HIGH priority, continuous stream")
    print("  1 machine\n")
    
    tasks = [
        Task('L', 0, 4, Priority.LOW, 20),  # deadline window = 20
        Task('H1', 0, 3, Priority.HIGH, 30),
        Task('H2', 3, 3, Priority.HIGH, 33),
        Task('H3', 6, 3, Priority.HIGH, 36),
        Task('H4', 9, 3, Priority.HIGH, 39),
        Task('H5', 12, 3, Priority.HIGH, 42),
    ]
    
    print("Deadline pressure calculation for L:")
    print("  At time 10: pressure = 10/20 = 0.50")
    print("  At time 14: pressure = 14/20 = 0.70")
    print("  At time 18: pressure = 18/20 = 0.90")
    print()
    
    alphas = [0.5, 0.7, 0.9]
    
    for alpha in alphas:
        dpe_tasks = copy.deepcopy(tasks)
        dpe = DPE_Scheduler(dpe_tasks, 1, alpha=alpha)
        dpe.run()
        
        task_l = [t for t in dpe_tasks if t.id == 'L'][0]
        elevation_time = alpha * 20  # When elevation should occur
        
        print(f"DPE (α={alpha}):")
        print(f"  Elevation threshold reached at time {elevation_time:.1f}")
        print(f"  L starts at time {task_l.start_time:.1f}")
        print(f"  L completes at time {task_l.completion_time:.1f}, deadline {task_l.deadline}")
        print(f"  Status: {'✅ MET' if task_l.meets_deadline() else '❌ MISSED'}")
        print()
    # Export results for this alpha run
    export_run_results(f'demo3_DPE_a{alpha}', dpe_tasks)


def create_harder_scenarios():
    """
    Create test cases that DEFINITELY show differences
    """
    print("\n" + "=" * 80)
    print("HARD TEST CASES FOR YOUR PROJECT")
    print("=" * 80)
    
    print("\n1. INFEASIBLE TEST CASE:")
    print("   (All algorithms should fail)")
    print("-" * 80)
    tasks = [
        # 4 tasks, each needs 5 time units
        # All have deadline = 5
        # But only 2 machines → impossible!
        Task(1, 0, 5, Priority.HIGH, 5),
        Task(2, 0, 5, Priority.HIGH, 5),
        Task(3, 0, 5, Priority.HIGH, 5),
        Task(4, 0, 5, Priority.HIGH, 5),
    ]
    print("   4 tasks × 5 time units each = 20 total time needed")
    print("   2 machines × deadline 5 = 10 time available")
    print("   20 > 10 → IMPOSSIBLE!\n")
    
    algorithms = [
        ("SPT", SPT_Scheduler),
        ("EDF", EDF_Scheduler),
        ("Priority-First", PriorityFirst_Scheduler),
        ("DPE", lambda t, m: DPE_Scheduler(t, m, alpha=0.7)),
    ]
    
    print(f"{'Algorithm':<20} | Deadline Misses | Success Rate")
    print("-" * 60)
    
    for name, SchedulerClass in algorithms:
        test_tasks = copy.deepcopy(tasks)
        scheduler = SchedulerClass(test_tasks, 2)
        scheduler.run()
        
        misses = sum(1 for t in test_tasks if not t.meets_deadline())
        rate = (len(test_tasks) - misses) / len(test_tasks) * 100
        
        print(f"{name:<20} | {misses}/4              | {rate:>6.1f}%")
    # Export per-algorithm results for infeasible test
    export_run_results(f'harder_infeasible_{name.replace(" ", "_")}', test_tasks)
    
    print("\n2. STARVATION TEST CASE:")
    print("   (Priority-First should fail low-priority)")
    print("-" * 80)
    
    tasks2 = [
        Task('LOW', 0, 6, Priority.LOW, 18),  # Will this get starved?
        Task('H1', 0, 3, Priority.HIGH, 25),
        Task('H2', 3, 3, Priority.HIGH, 28),
        Task('H3', 6, 3, Priority.HIGH, 31),
        Task('H4', 9, 3, Priority.HIGH, 34),
    ]
    
    print("   LOW task arrives at t=0, needs 6 time, deadline=18")
    print("   HIGH tasks keep arriving every 3 time units\n")
    
    print(f"{'Algorithm':<20} | LOW Status | LOW Complete Time")
    print("-" * 60)
    
    for name, SchedulerClass in algorithms:
        test_tasks = copy.deepcopy(tasks2)
        scheduler = SchedulerClass(test_tasks, 1)
        scheduler.run()
        
        low_task = [t for t in test_tasks if t.id == 'LOW'][0]
        status = "✅ MET" if low_task.meets_deadline() else "❌ MISSED"
        
        print(f"{name:<20} | {status:10} | {low_task.completion_time:.1f} (deadline {low_task.deadline})")
        # Export per-algorithm results for starvation test
        export_run_results(f'harder_starvation_{name.replace(" ", "_")}', test_tasks)


def export_run_results(run_name, tasks, out_dir='visual_results', filename='all_visual_results.csv'):
    """Append task run results into one CSV file. Creates `out_dir` if missing.

    The CSV file will contain a `run` column so multiple runs are combined.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)

    fieldnames = [
        'run', 'task_id', 'arrival_time', 'processing_time', 'priority', 'deadline',
        'start_time', 'completion_time', 'machine_id', 'met_deadline'
    ]

    write_header = not os.path.exists(path)

    try:
        with open(path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for t in tasks:
                writer.writerow({
                    'run': run_name,
                    'task_id': t.id,
                    'arrival_time': getattr(t, 'arrival_time', ''),
                    'processing_time': getattr(t, 'processing_time', ''),
                    'priority': getattr(t.priority, 'name', str(t.priority)),
                    'deadline': getattr(t, 'deadline', ''),
                    'start_time': getattr(t, 'start_time', ''),
                    'completion_time': getattr(t, 'completion_time', ''),
                    'machine_id': getattr(t, 'machine_id', ''),
                    'met_deadline': t.meets_deadline() if hasattr(t, 'meets_deadline') else ''
                })
    except Exception as e:
        print(f"Failed to append CSV for {run_name}: {e}")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║          VISUAL DEMONSTRATION OF ALGORITHM DIFFERENCES             ║
║                                                                    ║
║  This shows EXACTLY when and why algorithms make different        ║
║  scheduling decisions and produce different results.              ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    demo_case_1()  # SPT vs EDF
    demo_case_2()  # Priority-First vs DPE
    demo_case_3()  # Different α values
    create_harder_scenarios()  # Test cases for your project
    
    print("\n" + "=" * 80)
    print("💡 KEY TAKEAWAYS")
    print("=" * 80)
    print("""
1. SPT ignores deadlines → Can miss tight deadlines even when avoidable
2. EDF respects deadlines → Better for deadline-constrained systems
3. Priority-First is rigid → Can starve low-priority tasks indefinitely
4. DPE prevents starvation → Dynamically elevates based on deadline pressure
5. α parameter matters → Lower α = more aggressive, higher α = more conservative

For your project, use these patterns to create test cases that reveal when
your DPE algorithm provides value over the baselines!
    """)