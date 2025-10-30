"""
Challenging Test Cases for COMP3821 Scheduling Project
========================================================

These test cases are designed to:
1. Show differences between algorithms
2. Demonstrate when some algorithms fail
3. Highlight the value of DPE
4. Create infeasible scenarios

Each test case has a specific purpose to reveal algorithm behavior.
"""

import copy
from simple_simulator import (
    Task, Priority, 
    SPT_Scheduler, EDF_Scheduler, 
    PriorityFirst_Scheduler, DPE_Scheduler
)


# =============================================================================
# TEST CASE 1: SPT Ignores Deadlines (SPT SHOULD FAIL)
# =============================================================================

def test_case_1_spt_fails():
    """
    SPT will schedule shortest tasks first but ignore deadlines.
    Expected: SPT will miss deadlines, EDF will succeed
    """
    return [
        # Short task with loose deadline
        Task(1, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=30),
        
        # Long task with TIGHT deadline (should go first by EDF)
        Task(2, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=6),
        
        # Another short task
        Task(3, arrival_time=0, processing_time=1, priority=Priority.HIGH, deadline=25),
        
        # Long task with tight deadline
        Task(4, arrival_time=0, processing_time=4, priority=Priority.HIGH, deadline=5),
    ], 2


# =============================================================================
# TEST CASE 2: Priority-First Causes Starvation (PRIORITY SHOULD FAIL LOW)
# =============================================================================

def test_case_2_starvation():
    """
    Continuous high-priority tasks starve low-priority tasks.
    Expected: Priority-First fails low tasks, DPE saves them
    """
    return [
        # Low-priority task arrives early with tight deadline
        Task(1, arrival_time=0, processing_time=3, priority=Priority.LOW, deadline=8),
        
        # Stream of high-priority tasks
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=15),
        Task(3, arrival_time=1, processing_time=2, priority=Priority.HIGH, deadline=16),
        Task(4, arrival_time=2, processing_time=2, priority=Priority.HIGH, deadline=17),
        Task(5, arrival_time=3, processing_time=2, priority=Priority.HIGH, deadline=18),
        
        # Another low-priority with tight deadline
        Task(6, arrival_time=1, processing_time=3, priority=Priority.LOW, deadline=10),
    ], 2


# =============================================================================
# TEST CASE 3: Truly Infeasible (ALL SHOULD FAIL)
# =============================================================================

def test_case_3_impossible():
    """
    Mathematically impossible to meet all deadlines.
    Expected: All algorithms fail some tasks
    """
    return [
        # All arrive at once, all have very tight deadlines
        Task(1, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=5),
        Task(2, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=5),
        Task(3, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=5),
        Task(4, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=5),
    ], 2  # Only 2 machines, need 4 to succeed


# =============================================================================
# TEST CASE 4: DPE α Value Matters (SHOW DIFFERENT α RESULTS)
# =============================================================================

def test_case_4_alpha_sensitivity():
    """
    Test case where different DPE α thresholds give different results.
    Expected: Lower α (more aggressive) helps low-priority tasks more
    """
    return [
        # Low-priority task with moderately tight deadline
        Task(1, arrival_time=0, processing_time=4, priority=Priority.LOW, deadline=12),
        
        # High-priority tasks that delay it
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=20),
        Task(3, arrival_time=1, processing_time=2, priority=Priority.HIGH, deadline=22),
        Task(4, arrival_time=2, processing_time=2, priority=Priority.HIGH, deadline=24),
        
        # Another low-priority
        Task(5, arrival_time=1, processing_time=3, priority=Priority.LOW, deadline=15),
    ], 2


# =============================================================================
# TEST CASE 5: Priority Inversion Problem (PRIORITY-FIRST FAILS)
# =============================================================================

def test_case_5_priority_inversion():
    """
    Low-priority task blocks machine, high-priority misses deadline.
    Expected: Priority-First may fail if low-priority task already running
    """
    return [
        # Low-priority long task starts first
        Task(1, arrival_time=0, processing_time=8, priority=Priority.LOW, deadline=30),
        
        # High-priority urgent task arrives AFTER low-priority starts
        Task(2, arrival_time=2, processing_time=3, priority=Priority.HIGH, deadline=6),
        
        # More high-priority tasks
        Task(3, arrival_time=3, processing_time=2, priority=Priority.HIGH, deadline=8),
    ], 1  # Single machine makes this interesting


# =============================================================================
# TEST CASE 6: Heavy Overload (MOST SHOULD FAIL MANY)
# =============================================================================

def test_case_6_overload():
    """
    Way too many tasks for available machines.
    Expected: All algorithms fail, but some fail more gracefully
    """
    tasks = []
    
    # 15 tasks, all tight deadlines
    for i in range(8):
        tasks.append(
            Task(i+1, arrival_time=i*0.5, processing_time=3, 
                 priority=Priority.HIGH, deadline=i*0.5 + 5)
        )
    
    for i in range(7):
        tasks.append(
            Task(i+9, arrival_time=i*0.5, processing_time=4, 
                 priority=Priority.LOW, deadline=i*0.5 + 10)
        )
    
    return tasks, 3  # Only 3 machines for 15 tasks


# =============================================================================
# TEST CASE 7: Sequential High-Priority Arrivals (TESTS FAIRNESS)
# =============================================================================

def test_case_7_fairness():
    """
    Low-priority task waits while high-priority keep arriving.
    Expected: DPE eventually elevates low-priority, Priority-First doesn't
    """
    return [
        # Low-priority task at start
        Task(1, arrival_time=0, processing_time=5, priority=Priority.LOW, deadline=20),
        
        # High-priority tasks keep arriving every 2 time units
        Task(2, arrival_time=1, processing_time=3, priority=Priority.HIGH, deadline=25),
        Task(3, arrival_time=3, processing_time=3, priority=Priority.HIGH, deadline=27),
        Task(4, arrival_time=5, processing_time=3, priority=Priority.HIGH, deadline=29),
        Task(5, arrival_time=7, processing_time=3, priority=Priority.HIGH, deadline=31),
        Task(6, arrival_time=9, processing_time=3, priority=Priority.HIGH, deadline=33),
    ], 2


# =============================================================================
# TEST CASE 8: Deadline Clustering (TESTS TIE-BREAKING)
# =============================================================================

def test_case_8_tie_breaking():
    """
    Multiple tasks with same deadline but different processing times.
    Expected: SPT and EDF will make different choices
    """
    return [
        # All have deadline of 10, but different processing times
        Task(1, arrival_time=0, processing_time=1, priority=Priority.HIGH, deadline=10),
        Task(2, arrival_time=0, processing_time=5, priority=Priority.HIGH, deadline=10),
        Task(3, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=10),
        Task(4, arrival_time=0, processing_time=4, priority=Priority.HIGH, deadline=10),
        
        # Low-priority with tighter deadline
        Task(5, arrival_time=0, processing_time=3, priority=Priority.LOW, deadline=8),
    ], 2


# =============================================================================
# TEST CASE 9: DPE Pressure Calculation Edge Case
# =============================================================================

def test_case_9_dpe_edge_case():
    """
    Low-priority task where DPE elevation happens at different times.
    Expected: α=0.5 elevates earlier than α=0.9
    """
    return [
        # Low-priority task: deadline window = 20-0 = 20
        # At time 10: pressure = 10/20 = 0.5 (α=0.5 elevates)
        # At time 14: pressure = 14/20 = 0.7 (α=0.7 elevates)
        # At time 18: pressure = 18/20 = 0.9 (α=0.9 elevates)
        Task(1, arrival_time=0, processing_time=4, priority=Priority.LOW, deadline=20),
        
        # High-priority tasks that delay it
        Task(2, arrival_time=0, processing_time=3, priority=Priority.HIGH, deadline=25),
        Task(3, arrival_time=3, processing_time=3, priority=Priority.HIGH, deadline=28),
        Task(4, arrival_time=6, processing_time=3, priority=Priority.HIGH, deadline=31),
        Task(5, arrival_time=9, processing_time=3, priority=Priority.HIGH, deadline=34),
    ], 1  # Single machine to force sequential execution


# =============================================================================
# TEST CASE 10: Mixed Priorities with Complex Dependencies
# =============================================================================

def test_case_10_complex():
    """
    Complex scenario with mixture of everything.
    Expected: Clear performance differences between algorithms
    """
    return [
        # Early low-priority with tight deadline
        Task(1, arrival_time=0, processing_time=6, priority=Priority.LOW, deadline=15),
        
        # High-priority with various urgencies
        Task(2, arrival_time=0, processing_time=2, priority=Priority.HIGH, deadline=5),
        Task(3, arrival_time=1, processing_time=4, priority=Priority.HIGH, deadline=12),
        Task(4, arrival_time=2, processing_time=1, priority=Priority.HIGH, deadline=8),
        
        # More low-priority tasks
        Task(5, arrival_time=3, processing_time=5, priority=Priority.LOW, deadline=18),
        Task(6, arrival_time=4, processing_time=3, priority=Priority.LOW, deadline=20),
        
        # Late arriving high-priority
        Task(7, arrival_time=6, processing_time=2, priority=Priority.HIGH, deadline=14),
        Task(8, arrival_time=8, processing_time=3, priority=Priority.HIGH, deadline=16),
    ], 3


# =============================================================================
# RUN ALL TEST CASES
# =============================================================================

def run_single_test_case(test_name, tasks, num_machines, algorithms):
    """Run one test case with all algorithms"""
    
    print("\n" + "=" * 100)
    print(f"TEST CASE: {test_name}")
    print("=" * 100)
    
    results = []
    
    for algo_name, SchedulerClass, kwargs in algorithms:
        # Create fresh task copies
        tasks_copy = copy.deepcopy(tasks)
        
        # Run scheduler
        try:
            scheduler = SchedulerClass(tasks_copy, num_machines, **kwargs)
            scheduler.run()
            
            # Calculate metrics
            high_priority = [t for t in tasks_copy if t.priority == Priority.HIGH]
            low_priority = [t for t in tasks_copy if t.priority == Priority.LOW]
            
            high_met = sum(1 for t in high_priority if t.meets_deadline())
            low_met = sum(1 for t in low_priority if t.meets_deadline())
            total_met = high_met + low_met
            
            makespan = max((t.completion_time for t in tasks_copy if t.completion_time), default=0)
            
            high_rate = (high_met / len(high_priority) * 100) if high_priority else 100
            low_rate = (low_met / len(low_priority) * 100) if low_priority else 100
            total_rate = (total_met / len(tasks_copy) * 100) if tasks_copy else 100
            
            results.append({
                'algorithm': algo_name,
                'high_rate': high_rate,
                'low_rate': low_rate,
                'total_rate': total_rate,
                'makespan': makespan,
                'high_met': high_met,
                'high_total': len(high_priority),
                'low_met': low_met,
                'low_total': len(low_priority)
            })
            
        except Exception as e:
            print(f"❌ {algo_name} FAILED: {str(e)}")
            results.append({
                'algorithm': algo_name,
                'high_rate': 0,
                'low_rate': 0,
                'total_rate': 0,
                'makespan': float('inf'),
                'high_met': 0,
                'high_total': 0,
                'low_met': 0,
                'low_total': 0
            })
    
    # Print comparison table
    print("\nRESULTS COMPARISON:")
    print("-" * 100)
    print(f"{'Algorithm':<20} | {'High Priority':<20} | {'Low Priority':<20} | {'Total':<12} | {'Makespan':<10}")
    print("-" * 100)
    
    for r in results:
        high_str = f"{r['high_met']}/{r['high_total']} ({r['high_rate']:.1f}%)"
        low_str = f"{r['low_met']}/{r['low_total']} ({r['low_rate']:.1f}%)"
        
        # Color code results
        status = ""
        if r['high_rate'] < 100:
            status = "⚠️ HIGH FAIL"
        elif r['low_rate'] < 100:
            status = "⚠️ LOW FAIL"
        else:
            status = "✅ ALL PASS"
        
        print(f"{r['algorithm']:<20} | {high_str:<20} | {low_str:<20} | {r['total_rate']:>6.1f}% | {r['makespan']:>8.1f}  {status}")
    
    # Highlight differences
    print("\n📊 KEY OBSERVATIONS:")
    
    # Find best and worst
    best_total = max(r['total_rate'] for r in results)
    worst_total = min(r['total_rate'] for r in results)
    
    if best_total > worst_total:
        best_algo = [r['algorithm'] for r in results if r['total_rate'] == best_total]
        worst_algo = [r['algorithm'] for r in results if r['total_rate'] == worst_total]
        print(f"   • Best: {', '.join(best_algo)} ({best_total:.1f}%)")
        print(f"   • Worst: {', '.join(worst_algo)} ({worst_total:.1f}%)")
    else:
        print(f"   • All algorithms performed equally ({best_total:.1f}%)")
    
    # Check low-priority performance
    low_rates = [r['low_rate'] for r in results if r['low_total'] > 0]
    if low_rates:
        best_low = max(low_rates)
        worst_low = min(low_rates)
        if best_low > worst_low:
            print(f"   • Low-priority protection varies: {worst_low:.1f}% to {best_low:.1f}%")
    
    return results


def run_all_challenging_tests():
    """Run all challenging test cases"""
    
    print("╔" + "=" * 98 + "╗")
    print("║" + " " * 30 + "CHALLENGING TEST CASES" + " " * 46 + "║")
    print("║" + " " * 25 + "Revealing Algorithm Differences" + " " * 42 + "║")
    print("╚" + "=" * 98 + "╝")
    
    # Define algorithms to test
    algorithms = [
        ('SPT', SPT_Scheduler, {}),
        ('EDF', EDF_Scheduler, {}),
        ('Priority-First', PriorityFirst_Scheduler, {}),
        ('DPE (α=0.5)', DPE_Scheduler, {'alpha': 0.5}),
        ('DPE (α=0.7)', DPE_Scheduler, {'alpha': 0.7}),
        ('DPE (α=0.9)', DPE_Scheduler, {'alpha': 0.9}),
    ]
    
    # Define test cases with descriptions
    test_cases = [
        ("1. SPT Ignores Deadlines", 
         "SPT schedules short tasks first, missing tight deadlines",
         test_case_1_spt_fails),
        
        ("2. Starvation Scenario", 
         "Continuous high-priority tasks starve low-priority",
         test_case_2_starvation),
        
        ("3. Impossible Deadlines", 
         "Mathematically infeasible - all algorithms should fail",
         test_case_3_impossible),
        
        ("4. DPE Alpha Sensitivity", 
         "Different α values produce different results",
         test_case_4_alpha_sensitivity),
        
        ("5. Priority Inversion", 
         "Low-priority task blocks high-priority on single machine",
         test_case_5_priority_inversion),
        
        ("6. Heavy Overload", 
         "Too many tasks, test graceful degradation",
         test_case_6_overload),
        
        ("7. Fairness Test", 
         "Sequential arrivals test fairness to low-priority",
         test_case_7_fairness),
        
        ("8. Tie-Breaking", 
         "Same deadlines, different processing times",
         test_case_8_tie_breaking),
        
        ("9. DPE Timing", 
         "When exactly does DPE elevation occur?",
         test_case_9_dpe_edge_case),
        
        ("10. Complex Mixed", 
         "Realistic scenario with all challenges",
         test_case_10_complex),
    ]
    
    all_results = {}
    
    for test_name, description, test_func in test_cases:
        tasks, num_machines = test_func()
        
        print(f"\n\n{'='*100}")
        print(f"📋 {test_name}")
        print(f"   {description}")
        print(f"   Tasks: {len(tasks)}, Machines: {num_machines}")
        print(f"{'='*100}")
        
        results = run_single_test_case(test_name, tasks, num_machines, algorithms)
        all_results[test_name] = results
    
    # Print overall summary
    print("\n\n" + "=" * 100)
    print("🏆 OVERALL SUMMARY")
    print("=" * 100)
    
    algorithm_wins = {algo: 0 for algo, _, _ in algorithms}
    
    for test_name, results in all_results.items():
        best_rate = max(r['total_rate'] for r in results)
        winners = [r['algorithm'] for r in results if r['total_rate'] == best_rate]
        for winner in winners:
            algorithm_wins[winner] += 1
    
    print("\nTimes each algorithm was best (or tied for best):")
    for algo, wins in sorted(algorithm_wins.items(), key=lambda x: x[1], reverse=True):
        print(f"   {algo:<20}: {wins}/10")
    
    print("\n" + "=" * 100)
    print("💡 KEY INSIGHTS:")
    print("=" * 100)
    print("1. SPT fails when deadlines are tight (Test Case 1)")
    print("2. Priority-First can starve low-priority tasks (Test Case 2, 7)")
    print("3. DPE prevents starvation with dynamic elevation (Test Case 2, 7)")
    print("4. Different α values matter - lower α = more aggressive elevation (Test Case 4, 9)")
    print("5. All algorithms struggle under overload, but some degrade better (Test Case 6)")
    print("6. EDF is solid for deadline-focused scheduling (multiple cases)")
    print("=" * 100)


if __name__ == "__main__":
    run_all_challenging_tests()