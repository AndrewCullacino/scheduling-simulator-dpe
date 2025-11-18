# Presentation Script: Greedy Scheduling with Dynamic Priority Elevations and Deadlines

**Group 5 | COMP3821 Project Presentation**
Jintian Wang (z5536837), Dennis Shu (z5522609), Evan Lin (z5589313)
Mentor: Ayda Valinezhad Orang

---

## Slide 1: Title Slide (30 seconds)

**Visual**: Title, team members, group number

**Script**:
"Good [morning/afternoon], everyone. I'm [Name] from Group 5, and today we'll present our research on Greedy Scheduling with Dynamic Priority Elevations and Deadlines. My teammates are [introduce briefly], and we were mentored by Ayda Valinezhad Orang."

---

## Slide 2: Problem Overview (1 minute)

**Visual**: Problem formalization diagram or bullet points

**Script**:
"Our research tackles parallel machine scheduling with priority classes and deadlines. Imagine a cloud computing environment where you have premium customers requiring urgent service and standard customers with routine tasks. How do you schedule them efficiently without starving lower-priority work?

We formalized this as: n tasks, m identical parallel machines, two priority classes (high and low), with strict deadlines. The challenge is minimizing makespan while preventing low-priority task starvation."

**Key Points to Emphasize**:
- Real-world applications: cloud computing, emergency departments
- Two priority classes with different deadlines
- Non-preemptive scheduling constraint

---

## Slide 3: Algorithms Tested (1.5 minutes)

**Visual**: List of 4 algorithms with brief descriptions

**Script**:
"We implemented and evaluated four scheduling algorithms:

1. **SPT - Shortest Processing Time First**: Schedules tasks by increasing processing time. Optimal for minimizing average completion time.

2. **EDF - Earliest Deadline First**: Prioritizes tasks by deadline urgency. Theoretically optimal for single-processor real-time systems.

3. **Priority-First**: Strict priority ordering - all high-priority tasks before any low-priority tasks. Guarantees high-priority performance but risks starvation.

4. **DPE - Dynamic Priority Elevation**: Our novel mechanism that temporarily promotes low-priority tasks when they've consumed more than α (alpha) threshold of their deadline window. We tested three α values: 0.5, 0.7, and 0.9.

All algorithms have O(n log n) time complexity and O(n+m) space complexity."

**Key Points to Emphasize**:
- DPE was our hypothesis for preventing starvation
- α parameter controls when elevation triggers
- All algorithms theoretically sound

---

## Slide 4: Critical Discovery - EDF Bug (2 minutes)

**Visual**: Diagram showing bug behavior, before/after comparison table

**Script**:
"During validation, we made a critical discovery that fundamentally changed our results. We noticed EDF was producing identical schedules to SPT despite having completely different theoretical foundations. This was highly suspicious.

**The Bug**: Our initial implementation processed arrival events one-by-one, immediately calling the scheduler after each arrival. When multiple tasks arrived simultaneously - like at time zero in batch scenarios - the first task would be scheduled before other tasks even entered the ready queue. This forced EDF to behave exactly like SPT.

**The Fix**: We modified event processing to: (1) collect ALL events at the current timestamp, (2) process all ARRIVAL events before COMPLETION events, and (3) call the scheduler only AFTER all events are processed. This ensures EDF's selection function sees all available tasks when making deadline-based decisions.

**Impact**: After the fix, EDF showed dramatically improved performance:
- Extreme 1: Success rate jumped from 85.7% to 100%
- Extreme 3: Success rate improved from 75% to 100%, and makespan improved from 12 to 10 - that's 16.7% better!

This taught us a crucial lesson: Implementation quality dominates algorithmic sophistication. A correctly implemented simple algorithm beats a poorly implemented sophisticated one."

**Key Points to Emphasize**:
- Bug was subtle but critical
- Demonstrates importance of rigorous testing
- Shows gap between theory and implementation
- After fix, all results scientifically valid

---

## Slide 5: Comprehensive Results (2 minutes)

**Visual**: `makespan_comparison_detailed.png` - the main results chart

**Script**:
"After fixing the EDF bug, we re-ran all 84 experiments - that's 14 scenarios times 6 algorithm variants. Here's what we found:

**Overall Performance**:
- **EDF emerged as the best overall performer**: Lowest average makespan of 12.1 and highest success rate of 91.7%
- **SPT won only 1 out of 14 scenarios**: The Batch Arrival scenario where it achieved 7.1% better makespan
- **DPE never outperformed any baseline**: Zero wins across all 14 scenarios and all three α parameter values

Most striking: In 11 out of 14 scenarios - that's 79% of our test cases - all algorithms performed identically. This demonstrates a fundamental insight: when systems are well-provisioned with adequate resources, algorithmic sophistication becomes irrelevant."

**Key Points to Emphasize**:
- Comprehensive evaluation: 84 experimental runs
- DPE's complete lack of advantage (0/14)
- Resource provisioning dominates algorithm choice

---

## Slide 6: Example - Batch Arrival (SPT Advantage) (1.5 minutes)

**Visual**: Side-by-side Gantt charts - `Batch_Arrival_SPT_gantt.png` and `Batch_Arrival_EDF_gantt.png`

**Script**:
"Let's look at the one scenario where algorithm choice actually mattered in SPT's favor.

**Batch Arrival Scenario**: All tasks arrive simultaneously at time zero. Both algorithms achieve 100% deadline success, but SPT completes with makespan 13 while EDF takes 14 - that's 7.1% better for SPT.

**Why does SPT win here?** When all tasks arrive together, SPT's strategy of scheduling shortest tasks first minimizes idle time and packs tasks efficiently. EDF, prioritizing by deadline, doesn't optimize for this simultaneous arrival pattern.

**Takeaway**: SPT excels for batch processing scenarios where tasks arrive together."

**Key Points to Emphasize**:
- Both achieve 100% success
- Difference is in makespan efficiency
- Context-specific advantage

---

## Slide 7: Example - Extreme 3 (EDF Advantage) (1.5 minutes)

**Visual**: Side-by-side Gantt charts - `Extreme_3_SPT_gantt.png` and `Extreme_3_EDF_gantt.png`

**Script**:
"Now the opposite case - where EDF dominates.

**Extreme 3 Scenario**: Designed to stress-test SPT's deadline blindness. SPT achieves only 75% success rate with makespan 12, while EDF achieves 100% success with makespan 10 - that's 16.7% better!

**What's happening?** Look at the SPT Gantt chart - you can see Task T2 with a red deadline-missed border. SPT scheduled it late because it had a longer processing time, completely ignoring its urgent deadline. EDF, aware of deadlines, schedules T2 earlier, ensuring all tasks meet their constraints while also achieving better makespan.

**Takeaway**: EDF excels for deadline-critical systems where meeting time constraints is paramount."

**Key Points to Emphasize**:
- Both success rate AND makespan favor EDF
- SPT's deadline blindness causes failures
- Visual evidence in Gantt charts

---

## Slide 8: Why DPE Failed (2 minutes)

**Visual**: Analysis breakdown diagram

**Script**:
"Our most significant finding is actually a negative result: DPE provided zero advantage. Let me explain why this happened and why it's scientifically valuable.

**Four Primary Factors**:

1. **Resource Abundance (Primary Factor)**: In 79% of scenarios, machine capacity sufficiently exceeded task demands. When well-provisioned, scheduling strategy becomes irrelevant - all algorithms achieve optimal results. This demonstrates that resource provisioning dominates algorithmic sophistication.

2. **Test Scenario Limitations**: Our scenarios may lack conditions creating sufficient deadline pressure for DPE elevation to provide value. Most tasks arrived at time zero (batch arrivals) rather than continuously. Higher utilization scenarios with 90%+ capacity and dynamic arrival patterns might show different results.

3. **Non-Preemptive Constraints**: Once a task starts, it cannot be interrupted. DPE cannot elevate tasks that haven't arrived yet, and cannot preempt running tasks. This creates fundamental mathematical barriers no scheduling algorithm can overcome.

4. **α Parameter Insensitivity**: Testing α at 0.5, 0.7, and 0.9 produced no observable differences, suggesting either insufficient deadline pressure or potential issues with our elevation mechanism.

**Scientific Value**: Negative results are valuable when methodology is rigorous and conclusions are clear. Our findings guide practitioners toward proven strategies and adequate resource provisioning rather than algorithmic complexity."

**Key Points to Emphasize**:
- Negative results have scientific value
- Resource provisioning matters more than algorithms
- Identifies conditions where DPE might work (future work)

---

## Slide 9: Practical Recommendations (1.5 minutes)

**Visual**: Recommendation summary with icons/bullets

**Script**:
"Based on our comprehensive evaluation, we provide clear guidance for practitioners:

**1. Provision Resources First**: In 79% of our scenarios, algorithm choice was irrelevant when capacity exceeded demands. Before optimizing algorithms, ensure adequate machine capacity. Monitor utilization and consider expansion at 90%+.

**2. Choose Context-Specific Algorithms**:
- Use SPT for batch processing scenarios where tasks arrive simultaneously
- Use EDF for deadline-critical systems where meeting time constraints is paramount
- Use Priority-First only when strict priority ordering is mandatory for correctness

**3. Avoid Premature Optimization**: Complex dynamic mechanisms like DPE add implementation complexity and testing burden without demonstrated benefit in typical scenarios. Start simple.

**4. Prioritize Implementation Quality**: The EDF bug invalidated our initial results. Correct implementation of simple algorithms outperforms buggy implementation of sophisticated approaches. Invest in rigorous testing and validation.

These recommendations are evidence-based, derived from 84 experimental runs across diverse scenarios."

**Key Points to Emphasize**:
- Actionable guidance for real systems
- Evidence-based (not theoretical)
- Implementation quality over sophistication

---

## Slide 10: Conclusions & Future Work (1.5 minutes)

**Visual**: Summary bullets and future directions

**Script**:
"To conclude:

**Key Contributions**:
1. Comprehensive experimental evaluation demonstrating resource provisioning dominates algorithmic sophistication
2. Negative result documentation showing DPE provides no advantage, guiding practitioners toward proven strategies
3. Critical implementation validation discovering and fixing an EDF bug that improved success rates by up to 25 percentage points
4. Theoretical analysis including SPT optimality proof and time complexity analysis

**Lessons Learned**: Evidence-based algorithm selection outperforms complexity for its own sake. Simple, proven, context-appropriate strategies excel in their target contexts.

**Future Research Directions**:
- DPE-focused scenarios with higher utilization (90%+ capacity)
- Continuous arrival patterns with dynamic workloads
- Preemptive scheduling variants to test if preemption enables DPE advantages
- Extension to k priority classes (k > 2)
- Real workload traces from cloud computing and manufacturing systems

Our research demonstrates that negative results provide valuable scientific contributions when methodology is rigorous and conclusions are actionable. Thank you for your attention. We're happy to answer questions."

**Key Points to Emphasize**:
- Research contributes despite negative DPE result
- Clear future work directions
- Scientific rigor maintained throughout

---

## Slide 11: Q&A Preparation

**Potential Questions & Answers**:

**Q: "Why didn't you test higher utilization scenarios?"**
A: "Excellent question. Our scenarios were designed for comprehensive coverage across different conditions, but you're right that higher utilization (90%+) might reveal DPE advantages. That's explicitly listed in our future work. The challenge is designing realistic scenarios that maintain that pressure sustainably."

**Q: "Could the DPE implementation itself be buggy?"**
A: "That's possible. The α parameter insensitivity does suggest potential issues. However, we validated DPE's elevation logic was triggering when expected - the issue is more that our scenarios didn't create conditions where elevation provided value. Future work should validate the mechanism more thoroughly with targeted stress tests."

**Q: "How did you decide on the α values?"**
A: "We chose 0.5, 0.7, and 0.9 to cover a range from conservative (elevating early at 50% deadline consumption) to aggressive (waiting until 90%). This range should capture different trade-offs between starvation prevention and priority guarantee strength. The fact that all three performed identically suggests deadline pressure was insufficient across all values."

**Q: "What about heterogeneous machines?"**
A: "Our study focused on identical parallel machines to isolate the effects of scheduling strategy from machine capability differences. Heterogeneous machines add another dimension of complexity - task-to-machine matching - which would confound our algorithm comparison. That's an excellent direction for future research."

**Q: "How long did the experiments take to run?"**
A: "The simulations themselves are very fast - microseconds per scenario due to discrete-event simulation efficiency. The time-consuming part was scenario design, implementation validation (especially finding the EDF bug!), and result analysis. Total project time was approximately [X weeks]."

**Q: "Could you explain the EDF bug fix more technically?"**
A: "Certainly. The bug was in lines 100-128 of simple_simulator.py. Original code had:
```python
for event in events:
    if event.type == ARRIVAL:
        ready_queue.add(event.task)
        schedule_ready_tasks()  # Called too early!
```
Fixed code:
```python
arrivals = [e for e in events if e.type == ARRIVAL]
for event in arrivals:
    ready_queue.add(event.task)
schedule_ready_tasks()  # Called after all arrivals
```
This ensures batch decisions see all available tasks."

**Q: "What was the most surprising finding?"**
A: "The most surprising was actually how often algorithm choice didn't matter - 79% of scenarios showed identical performance. We expected more differentiation. This taught us that practical systems engineering often reduces to resource provisioning over algorithmic sophistication. The EDF bug was also surprising in how subtle yet critical it was."

---

## Presentation Tips

**Timing**:
- Total target: 12-15 minutes
- Leave 3-5 minutes for Q&A
- Practice with timer

**Delivery**:
- Make eye contact, don't read slides
- Use visualizations to tell the story
- Point to specific features in Gantt charts
- Pause after key findings for emphasis

**Team Coordination**:
- Decide who presents which sections
- Practice transitions between speakers
- Have backup speaker for each section
- Designate Q&A coordinator

**Technical Terms**:
- Define on first use (makespan, etc.)
- Use analogies for complex concepts
- Avoid jargon when possible

**Emphasis Points**:
- 16.7% improvement (EDF advantage)
- 0/14 DPE wins (negative result)
- 79% scenarios identical (provisioning matters)
- EDF bug fix impact (25 percentage point improvement)

---

## Backup Slides (if time permits or for Q&A)

### Backup: Theoretical Foundation

**Content**: SPT optimality proof, complexity analysis details

**When to use**: If asked about theoretical rigor

### Backup: All Scenario Results

**Content**: Table of all 14 scenarios with detailed metrics

**When to use**: If asked about specific scenarios not covered

### Backup: DPE Algorithm Details

**Content**: Pseudocode, deadline pressure formula, elevation mechanism

**When to use**: If asked for DPE implementation specifics

### Backup: Experimental Setup

**Content**: Simulator architecture, event-driven model, validation methodology

**When to use**: If asked about reproducibility or validation

---

## Post-Presentation Checklist

- [ ] Upload presentation slides to course portal
- [ ] Submit final report PDF
- [ ] Submit poster PDF
- [ ] Upload code repository link
- [ ] Complete peer evaluation forms
- [ ] Thank mentor in follow-up email

**Repository Link Placeholder**: `https://github.com/[INSERT-REPOSITORY-URL]/comp3821-scheduling`

---

*End of Presentation Script*
