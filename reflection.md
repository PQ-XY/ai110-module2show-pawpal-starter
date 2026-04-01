# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    Owner — manages pets and their scheduler, stores personal contact info
    Pet — represents individual pets with species, breed, health info; records activities
    Scheduler — the algorithmic core that manages, prioritizes, and organizes all tasks
    Task — individual activities (feeding, walks, medications, appointments, etc.) with priority levels
    TaskType — enum defining the six main task categories

    Relationships:

        Owner owns multiple Pets (1:*)
        Owner has one Scheduler (1:1)
        Scheduler manages multiple Tasks (1:*)
        Tasks are assigned to specific Pets (*:1)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

**Yes, three key design decisions changed during implementation:**

**Change 1: Added `recurrence` field to Task class**
- *Original design*: Task was static—once created and completed, it was done.
- *Implementation change*: Added `recurrence: str` field (values: `None`, `"daily"`, `"weekly"`) to support repeating tasks.
- *Why*: Realistic pet care requires repeated tasks (daily feeding, weekly grooming). Without recurrence, owners would have to manually create thousands of task instances for a pet's lifetime. This field makes the system practical.

**Change 2: Conflict detection as warnings, not enforcement**
- *Original design*: Scheduler would "organize and prioritize" tasks but was vague on how to handle conflicts.
- *Implementation change*: Created `detect_conflicts()` as a separate method that returns warning messages rather than preventing task addition or auto-rescheduling.
- *Why*: We chose to let owners add conflicting tasks but alert them, rather than silently rejecting or auto-fixing schedules. This preserves owner control and transparency—important for a system managing pet health.

**Change 3: Updated Task.mark_complete() to accept Scheduler instance**
- *Original design*: `mark_complete()` was just a toggle; no mention of cascading effects.
- *Implementation change*: Modified signature to `mark_complete(self, scheduler: 'Scheduler' = None)` so that completing a recurring task automatically creates the next occurrence.
- *Why*: Without this, recurring tasks would disappear after completion and need manual re-creation. Passing the scheduler enables the Task to communicate back and trigger `create_next_occurrence()`.

**Overall rationale for changes:** The initial design was structurally sound but underspecified algorithmically. During implementation, we discovered that realistic pet scheduling needed three features not explicitly in the skeleton: recurrence handling, lightweight conflict detection, and task regeneration. These changes kept the object model clean while adding practical functionality.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

**Constraints implemented:**
1. **Time conflict** (primary): Tasks can't occur at the same time. Detects overlaps when:
   - Same pet has multiple tasks at identical time (impossible)
   - Different pets both need attention at identical time (owner can't do both)
2. **Completion status**: Only active (incomplete) tasks are checked for conflicts; completed tasks don't block scheduling
3. **Recurrence pattern**: Daily/weekly tasks automatically regenerate after completion, respecting the recurrence frequency
4. **Pet assignment**: Each task tied to a specific pet; conflicts are pet-aware
5. **Task priority**: Stored on each task but not yet used for conflict resolution (future enhancement)

**Constraints NOT implemented (but could be):**
- Task duration (we only check exact times, not time windows)
- Travel time between pets
- Owner availability preferences
- Pet-specific preferences or behaviors
- Task dependencies/sequencing
- Resource constraints beyond owner time

- How did you decide which constraints mattered most?

**Decision rationale:**
1. **Time conflicts first** — This is the hardest constraint to violate; it's logically impossible. An owner physically cannot walk two pets simultaneously. This was the highest priority.
2. **Completion status** — Completed tasks should never block new scheduling. Filtering active tasks keeps the system practical.
3. **Pet assignment** — Critical for linking tasks to specific animals; enables pet-level conflict detection.
4. **Recurrence** — Essential for realistic pet care (daily feeding, medication). Without it, the owner would manually re-add tasks constantly.
5. **Priority** — Deferred. While tasks have priority levels, we haven't implemented priority-based rescheduling yet. Time conflicts take absolute precedence over priority optimization.

**Trade-off made:** We chose *correctness over convenience*. The scheduler guarantees no logically impossible schedules (no double-booking), even if it means rejecting some schedules with warnings rather than auto-fixing them. This puts responsibility on the owner to manually resolve conflicts, which is safer than the system silently rescheduling tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

**Tradeoff: Exact time matching vs. duration-aware conflict detection**

- *What we chose*: Conflict detection only checks if two tasks occur at the **exact same time**. No consideration of task duration or time windows.
  - Example: A 30-minute walk (2PM–2:30PM) and a 1-hour walk (2:15PM–3:15PM) would NOT be flagged as conflicting because neither task has a duration field.

- *What we didn't choose*: A more complex duration-aware system that would detect overlapping time windows and warn about any minute of overlap.

**Why this tradeoff is reasonable for pet scheduling:**

1. **Simplicity & Speed**: Exact time matching is O(n) with a single pass; duration awareness would require interval overlap checks (O(n²) worst case). For a pet owner with 20-30 tasks/week, the simpler approach is sufficient.

2. **Pet care task patterns**: Most pet tasks in reality have **specific times, not durations**:
   - "Feed Max at 8:00 AM" (instantaneous action)
   - "Give Luna medication at 20:00" (quick action)
   - "Walk Buddy at 15:30" (owner's concern is the start time, not a locked 30-min window)
   - The owner will naturally leave time between tasks; they don't schedule walks back-to-back at 2:00, 2:15, 2:30.

3. **Owner flexibility**: If the owner realizes two tasks are too close together (e.g., walk at 2:00, grooming at 2:15), they can easily adjust by 15 minutes. The warning system gives them visibility to make this decision.

4. **Real-world precedent**: Most pet care apps and calendar systems use time-point scheduling, not time-window enforcement, for exactly this reason.

**Future enhancement**: If the system grew to include multiple pets and caregivers with strict time windows, duration-aware conflict detection would become necessary.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    design brainstorming, debugging, refactoring

- What kinds of prompts or questions were most helpful?
    prompts with details/examples

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

    **The UML diagram with Mermaid syntax**: The AI generated a detailed class diagram with note blocks showing relationships and method details. When I tried to render it, the diagram failed due to syntax errors in the note blocks.

- How did you evaluate or verify what the AI suggested?

    I tested the generated Mermaid code by attempting to render it. When it failed, I identified the problematic `note` syntax, simplified the diagram to remove those blocks, and re-rendered it successfully. This taught me that generated code needs validation before use—especially for specialized formats like Mermaid. I then verified the simplified version was semantically correct by comparing class names, attributes, and relationships to the actual implementation in `pawpal_system.py`.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

    1. **Sorting** — Tasks ordered chronologically by due_time
    2. **Filtering** — Tasks filtered by pet name and completion status (case-insensitive)
    3. **Recurring tasks** — Daily/weekly tasks generate next occurrence when marked complete
    4. **Conflict detection** — Same-pet and owner conflicts detected at identical times
    5. **Pet management** — Duplicate pets rejected, valid pets added; remove and reuse names

- Why were these tests important?

    - Sorting ensures the owner sees tasks in the right order throughout the day
    - Filtering lets owners focus on specific pets or pending work
    - Recurrence prevents manual re-creation of hundreds of tasks over a pet's lifetime
    - Conflict detection prevents logically impossible schedules (owner can't do two things at once)
    - Pet management prevents accidental duplicates and maintains data integrity

    All 32 tests pass, giving confidence that core scheduling logic is correct.

**b. Confidence**

- How confident are you that your scheduler works correctly?

    **⭐⭐⭐⭐⭐ (5/5 stars)** — All 32 tests pass, covering core features and edge cases. The four algorithms (sorting, filtering, recurrence, conflict detection) work correctly in isolation and integration. The duplicate pet prevention bug was identified and fixed with 8 additional tests. The system handles production scenarios: empty lists, single items, multiple pets, recurring tasks, and conflicts.

- What edge cases would you test next if you had more time?

    1. **Timezone handling** — Tasks across different timezones or daylight saving time transitions
    2. **Large-scale scheduling** — 100+ tasks, multiple owners, performance under load
    3. **Recurring task edge cases** — What happens if a daily task's date changes on leap day or month boundaries?
    4. **Concurrent updates** — Multiple users adding/completing tasks simultaneously
    5. **Task chains** — Dependencies (e.g., "medicate before walk") or prerequisite tasks
    6. **Owner/pet deletion** — Cascade behavior when removing an owner or pet with active tasks
    7. **Invalid recurrence patterns** — User enters "biweekly" or malformed recurrence strings

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    The backend logic.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I may try to incorporate LLM in the app for AI features.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I think we have to understand the what we need and always act as a leader in communicating with AI. 
