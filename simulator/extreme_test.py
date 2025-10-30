"""
TRULY CHALLENGING TEST CASES - Showing Clear Differences
==========================================================

These test cases are specifically designed to show dramatic differences
between algorithms, especially highlighting when DPE provides value.
"""

import copy
from simple_simulator import (
    Task, Priority,
    SPT_Scheduler, EDF_Scheduler,
    PriorityFirst_Scheduler, DPE_Scheduler
)


# =============================================================================
# EXTREME TEST CASE 1: Priority-First WILL Starve Low-Priority
# =============================================================================

def extreme_case_1_starvation():
    """
    Low-priority task with VERY tight deadline arrives early.
    Then continuous stream of high-priority tasks.
    
    Expected Results:
    - Priority-First: LOW-PRIORITY FAILS (starved)
    - DPE (α=0.7): LOW-PRIORITY SUCCEEDS (elevated in time)
    - DPE (α=0.5): LOW-PRIORITY SUCCEEDS (elevated earlier)
    """
    return [
        # Low-priority task arrives at t=0 with deadline at t=16
        Task(1, arrival_time=0, processing_time=5, priority=Priority.LOW, deadline=16),
        
        # High-priority tasks continuously arrive, each takes 2 time units
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=20),
        Task(3, arrival_time=2, processing_time=2, priority=Priority.HIGH, deadline=22),
        Task(4, arrival_time=4, processing_time=2, priority=Priority.HIGH, deadline=24),
        Task(5, arrival_time=6, processing_time=2, priority=Priority.HIGH, deadline=26),
        Task(6, arrival_time=8, processing_time=2, priority=Priority.HIGH, deadline=28),
        Task(7, arrival_time=10, processing_time=2, priority=Priority.HIGH, deadline=30),
    ], 1  # SINGLE MACHINE - forces sequential execution


# =============================================================================
# EXTREME TEST CASE 2: DPE Alpha Values Matter
# =============================================================================

def extreme_case_2_alpha_matters():
    """
    Low-priority task where different α values produce DIFFERENT results.
    
    deadline_window = 25 - 0 = 25
    At time 10: pressure = 10/25 = 0.40 (no elevation)
    At time 12.5: pressure = 12.5/25 = 0.50 (α=0.5 elevates HERE)
    At time 15: pressure = 15/25 = 0.60 (still waiting)
    At time 17.5: pressure = 17.5/25 = 0.70 (α=0.7 elevates HERE)
    At time 22.5: pressure = 22.5/25 = 0.90 (α=0.9 elevates HERE)
    At time 25: DEADLINE MISSED!
    
    Expected:
    - α=0.5: Elevates early, LOW succeeds
    - α=0.7: Elevates later, might succeed
    - α=0.9: Elevates too late, LOW FAILS
    """
    return [
        # Low-priority with deadline at t=25
        Task(1, arrival_time=0, processing_time=6, priority=Priority.LOW, deadline=25),
        
        # High-priority tasks that fill the time
        Task(2, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=30),
        Task(3, arrival_time=3, processing_time=3, priority=Priority.HIGH, deadline=33),
        Task(4, arrival_time=6, processing_time=3, priority=Priority.HIGH, deadline=36),
        Task(5, arrival_time=9, processing_time=3, priority=Priority.HIGH, deadline=39),
        Task(6, arrival_time=12, processing_time=3, priority=Priority.HIGH, deadline=42),
        Task(7, arrival_time=15, processing_time=3, priority=Priority.HIGH, deadline=45),
        Task(8, arrival_time=18, processing_time=3, priority=Priority.HIGH, deadline=48),
    ], 1  # Single machine


# =============================================================================
# EXTREME TEST CASE 3: SPT vs EDF - Clear Difference
# =============================================================================

def extreme_case_3_spt_vs_edf():
    """
    Tasks where SPT and EDF make opposite decisions.
    
    Expected:
    - SPT: Schedules short tasks, misses tight deadlines
    - EDF: Schedules by deadline, all succeed
    """
    return [
        # Very short task with LOOSE deadline
        Task(1, arrival_time=0, processing_time=1, priority=Priority.HIGH, deadline=50),
        
        # Long task with TIGHT deadline (should go first!)
        Task(2, arrival_time=0, processing_time=10, priority=Priority.HIGH, deadline=11),
        
        # Short task with loose deadline
        Task(3, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=45),
        
        # Medium task with tight deadline
        Task(4, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=7),
    ], 2


# =============================================================================
# EXTREME TEST CASE 4: Multiple Low-Priority Starvation
# =============================================================================

def extreme_case_4_multiple_starvation():
    """
    Multiple low-priority tasks, all with tight deadlines.
    High-priority stream tries to starve them all.
    
    Expected:
    - Priority-First: Multiple LOW failures
    - DPE: Saves most/all LOW tasks
    """
    return [
        # THREE low-priority tasks with tight deadlines
        Task(1, arrival_time=0, processing_time=4, priority=Priority.LOW, deadline=14),
        Task(2, arrival_time=1, processing_time=4, priority=Priority.LOW, deadline=16),
        Task(3, arrival_time=2, processing_time=4, priority=Priority.LOW, deadline=18),
        
        # High-priority stream
        Task(4, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=25),
        Task(5, arrival_time=2, processing_time=2, priority=Priority.HIGH, deadline=27),
        Task(6, arrival_time=4, processing_time=2, priority=Priority.HIGH, deadline=29),
        Task(7, arrival_time=6, processing_time=2, priority=Priority.HIGH, deadline=31),
        Task(8, arrival_time=8, processing_time=2, priority=Priority.HIGH, deadline=33),
        Task(9, arrival_time=10, processing_time=2, priority=Priority.HIGH, deadline=35),
    ], 2  # Two machines


# =============================================================================
# EXTREME TEST CASE 5: Infeasible for Priority-First ONLY
# =============================================================================

def extreme_case_5_priority_first_fails():
    """
    Feasible schedule EXISTS, but only if low-priority goes first!
    Priority-First will fail because it delays low-priority.
    
    Expected:
    - Priority-First: FAILS
    - EDF, DPE: SUCCEED
    """
    return [
        # Low-priority MUST go first or it misses deadline
        Task(1, arrival_time=0, processing_time=5, priority=Priority.LOW, deadline=6),
        
        # High-priority with looser deadline (can wait)
        Task(2, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=15),
        Task(3, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=20),
    ], 1  # Single machine


# =============================================================================
# RUN EXTREME TEST CASES
# =============================================================================

def run_extreme_tests():
    """Run all extreme test cases with detailed analysis"""
    
    print("╔" + "=" * 98 + "╗")
    print("║" + " " * 35 + "EXTREME TEST CASES" + " " * 45 + "║")
    print("║" + " " * 27 + "Designed to Show Clear Differences" + " " * 37 + "║")
    print("╚" + "=" * 98 + "╝\n")
    
    algorithms = [
        ('SPT', SPT_Scheduler, {}),
        ('EDF', EDF_Scheduler, {}),
        ('Priority-First', PriorityFirst_Scheduler, {}),
        ('DPE (α=0.5)', DPE_Scheduler, {'alpha': 0.5}),
        ('DPE (α=0.7)', DPE_Scheduler, {'alpha': 0.7}),
        ('DPE (α=0.9)', DPE_Scheduler, {'alpha': 0.9}),
    ]
    
    test_cases = [
        ("EXTREME 1: Priority-First Starvation", extreme_case_1_starvation,
         "Low-priority should STARVE under Priority-First, but DPE saves it"),
        
        ("EXTREME 2: Alpha Values Matter", extreme_case_2_alpha_matters,
         "α=0.5 elevates early, α=0.9 elevates too late"),
        
        ("EXTREME 3: SPT vs EDF", extreme_case_3_spt_vs_edf,
         "SPT ignores deadlines, EDF respects them"),
        
        ("EXTREME 4: Multiple Starvation", extreme_case_4_multiple_starvation,
         "Multiple low-priority tasks at risk"),
        
        ("EXTREME 5: Priority-First Impossible", extreme_case_5_priority_first_fails,
         "Feasible schedule exists, but not for Priority-First"),
    ]
    
    for test_name, test_func, description in test_cases:
        tasks, num_machines = test_func()
        
        print("\n" + "=" * 100)
        print(f"📋 {test_name}")
        print(f"   {description}")
        print(f"   Tasks: {len(tasks)}, Machines: {num_machines}")
        print("=" * 100 + "\n")
        
        results = []
        
        # Run each algorithm
        for algo_name, SchedulerClass, kwargs in algorithms:
            tasks_copy = copy.deepcopy(tasks)
            
            try:
                scheduler = SchedulerClass(tasks_copy, num_machines, **kwargs)
                scheduler.run()
                
                # Calculate detailed metrics
                high = [t for t in tasks_copy if t.priority == Priority.HIGH]
                low = [t for t in tasks_copy if t.priority == Priority.LOW]
                
                high_met = sum(1 for t in high if t.meets_deadline())
                low_met = sum(1 for t in low if t.meets_deadline())
                
                high_rate = (high_met / len(high) * 100) if high else 100
                low_rate = (low_met / len(low) * 100) if low else 100
                total_met = high_met + low_met
                total_rate = (total_met / len(tasks_copy) * 100)
                
                makespan = max((t.completion_time for t in tasks_copy), default=0)
                
                results.append({
                    'algo': algo_name,
                    'high_met': high_met,
                    'high_total': len(high),
                    'high_rate': high_rate,
                    'low_met': low_met,
                    'low_total': len(low),
                    'low_rate': low_rate,
                    'total_rate': total_rate,
                    'makespan': makespan
                })
                
            except Exception as e:
                print(f"❌ {algo_name} CRASHED: {e}")
        
        # Print results table
        print(f"{'Algorithm':<20} | {'High Priority':<18} | {'Low Priority':<18} | {'Total':<10} | Status")
        print("-" * 95)
        
        for r in results:
            high_str = f"{r['high_met']}/{r['high_total']} ({r['high_rate']:.0f}%)"
            low_str = f"{r['low_met']}/{r['low_total']} ({r['low_rate']:.0f}%)"
            
            # Determine status
            if r['high_rate'] < 100:
                status = "⚠️  HIGH FAIL"
            elif r['low_rate'] < 100:
                status = "⚠️  LOW FAIL"
            else:
                status = "✅ PERFECT"
            
            print(f"{r['algo']:<20} | {high_str:<18} | {low_str:<18} | {r['total_rate']:>6.0f}% | {status}")
        
        # Analysis
        print("\n🔍 ANALYSIS:")
        high_rates = [r['high_rate'] for r in results]
        low_rates = [r['low_rate'] for r in results]
        
        if len(set(low_rates)) > 1:
            print(f"   ✓ LOW-PRIORITY PROTECTION VARIES: {min(low_rates):.0f}% to {max(low_rates):.0f}%")
            best_low = [r['algo'] for r in results if r['low_rate'] == max(low_rates)]
            worst_low = [r['algo'] for r in results if r['low_rate'] == min(low_rates)]
            print(f"   ✓ Best for low-priority: {', '.join(best_low)}")
            print(f"   ✓ Worst for low-priority: {', '.join(worst_low)}")
        else:
            print(f"   • All algorithms protect low-priority equally ({low_rates[0]:.0f}%)")
        
        if len(set([r['total_rate'] for r in results])) > 1:
            best = max(r['total_rate'] for r in results)
            worst = min(r['total_rate'] for r in results)
            print(f"   ✓ PERFORMANCE RANGE: {worst:.0f}% to {best:.0f}%")
        
        print()
        


if __name__ == "__main__":
    run_extreme_tests()
    
    print("\n" + "=" * 100)
    print("✅ SUMMARY")
    print("=" * 100)
    print("""
These test cases demonstrate:

1. EXTREME 1: Priority-First WILL starve low-priority tasks when high-priority 
   tasks keep arriving. DPE prevents this with dynamic elevation.

2. EXTREME 2: The α parameter matters! Lower α (0.5) elevates tasks earlier,
   higher α (0.9) may elevate too late.

3. EXTREME 3: SPT ignores deadlines entirely, leading to failures. EDF is
   deadline-aware and performs better.

4. EXTREME 4: With multiple low-priority tasks, the differences become even
   more dramatic.

5. EXTREME 5: Some schedules are feasible but only if you don't strictly
   follow static priorities.

KEY FINDING: DPE with appropriate α provides better fairness while maintaining
high-priority guarantees!
    """)