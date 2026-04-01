# PawPal+ — Pet Care Task Scheduling System

**Version**: 1.0  
**Date**: March 31, 2026  
**Status**: ✅ Fully Functional

---

## Overview

**PawPal+** is an intelligent pet care task management system built with Streamlit and Python. It helps busy pet owners organize, track, and manage their pets' daily care routines with smart scheduling, automatic task recurrence, and conflict detection.

### Key Benefits

- 📅 **Automatic scheduling** — Create recurring daily/weekly tasks once, never manually re-enter them
- ⏰ **Chronological organization** — View tasks in order of when they need to happen
- 🔍 **Smart filtering** — Quickly find tasks by pet or completion status
- ⚠️ **Conflict prevention** — Get warned before scheduling impossible tasks (e.g., walking two pets at the same time)
- 📊 **Task dashboard** — See at a glance how many tasks are pending, completed, or recurring

### Project Scenario

A busy pet owner manages multiple pets with different care needs (feeding, walks, medication, grooming). They need:
- A way to track all pet care tasks efficiently
- Automatic scheduling of recurring activities
- Detection of conflicting schedules
- A clear daily plan organized by time

---

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd ai110-module2show-pawpal-starter
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate          # macOS/Linux
   # OR
   .venv\Scripts\activate             # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -m pytest tests/test_pawpal.py -v  # Run tests
   ```

---

## Quick Start

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the App

1. **Initialize Owner**: Enter owner information (name, email, phone, address)
2. **Add Pets**: Register each pet with species, breed, age, and health info
3. **Schedule Tasks**: Create tasks by selecting:
   - Pet
   - Task type (feeding, walk, medication, etc.)
   - Time
   - Priority (1-5 stars)
   - Recurrence (daily, weekly, or one-time)
4. **View Schedule**: Tasks display in chronological order in a sortable table
5. **Check Conflicts**: See yellow warnings for impossible schedules
6. **Filter Tasks**: Find specific pet's tasks or only pending/completed work
7. **Complete Tasks**: Mark tasks done; recurring tasks auto-generate next occurrence

---

## 📸 Demo

Here's the PawPal+ Streamlit app in action:

<a href="/course_images/ai110/Screenshot%202026-03-31%20at%2011.04.16%20PM.png" target="_blank"><img src='/course_images/ai110/Screenshot%202026-03-31%20at%2011.04.16%20PM.png' alt="PawPal+ Streamlit Interface Demo" width="100%" /></a>

The interface features:
- **Owner & Pet Management** — Register and manage pets with species, breed, age, and health info
- **Task Scheduling** — Create tasks with type, time, priority, and recurrence settings
- **Chronological View** — Tasks automatically sorted by time
- **Conflict Detection** — Yellow warnings for impossible schedules
- **Filtering** — Quick access to specific pet's tasks or pending/completed work
- **Task Dashboard** — Summary metrics showing total, pending, completed, and recurring tasks

---

## Architecture

PawPal+ uses a modular object-oriented design with four core classes:

### Class Diagram

See `pawpal_system.py` for the complete implementation. Key classes:

- **Owner** — Manages owner contact info and pet collection
- **Pet** — Represents individual pets with health tracking
- **Task** — Individual pet care activities (feeding, walks, meds, etc.)
- **Scheduler** — Core algorithmic engine for organizing and validating tasks
- **TaskType** — Enumeration of valid task categories

### Data Flow

```
User Input (Streamlit UI)
        ↓
App Handler (app.py)
        ↓
Scheduler Methods
├── sort_by_time()
├── filter_tasks()
├── detect_conflicts()
└── create_next_occurrence()
        ↓
Display Results (Tables, Warnings, Metrics)
```

---

## Core Features & Algorithms

PawPal+ implements four core scheduling algorithms to make pet care management efficient and conflict-free:

### 1. **Chronological Sorting** 
- **Algorithm**: Quick sort via Python's `sorted()` built-in
- **Complexity**: O(n log n) time, O(n) space
- **What it does**: Orders all active tasks by `due_time` from earliest to latest
- **Why it matters**: Owners see their schedule in the order tasks need to happen
- **Method**: `Scheduler.sort_by_time() → List[Task]`

### 2. **Flexible Task Filtering**
- **Algorithm**: Linear scan with conditional filtering
- **Complexity**: O(n) time, O(k) space (k = matching tasks)
- **What it does**: Filters tasks by pet name (case-insensitive) and/or completion status
- **Why it matters**: Quickly find tasks for a specific pet or see only pending/completed work
- **Method**: `Scheduler.filter_tasks(pet_name: str, completed: bool) → List[Task]`

### 3. **Recurring Task Management**
- **Algorithm**: Timedelta arithmetic for scheduling next occurrence
- **Complexity**: O(1) creation per recurrence
- **Recurrence patterns**:
  - `"daily"` → next task = today + 1 day at same time
  - `"weekly"` → next task = today + 7 days at same time
  - `None` → one-time task only
- **What it does**: Automatically generates the next occurrence when a recurring task is marked complete
- **Why it matters**: Eliminates manual re-entry for habits like daily feeding and weekly grooming
- **Methods**: 
  - `Task.mark_complete(scheduler: Scheduler): void` (triggers recurrence)
  - `Scheduler.create_next_occurrence(task: Task): void` (creates next instance)

### 4. **Lightweight Conflict Detection**
- **Algorithm**: Hash-based grouping by time, then conflict checking
- **Complexity**: O(n) time, O(n) space
- **What it detects**:
  - **Same-pet conflicts**: One pet can't have two tasks at the same time (physically impossible)
  - **Owner conflicts**: Owner can't manage multiple pets simultaneously (e.g., walk Max AND Luna at 3PM)
- **What it returns**: List of warning messages (non-blocking, allows owner to resolve manually)
- **Why it matters**: Prevents logically impossible schedules while giving the owner control to decide on rescheduling
- **Method**: `Scheduler.detect_conflicts() → List[str]`

---

## API Reference

### Scheduler Class

#### Methods

**`sort_by_time() → List[Task]`**
- Returns all active tasks sorted chronologically by due_time
- Example: `scheduler.sort_by_time()`

**`filter_tasks(pet_name: str = None, completed: bool = None) → List[Task]`**
- Filters tasks by pet name and/or completion status
- Example: `scheduler.filter_tasks(pet_name="Max", completed=False)`

**`detect_conflicts() → List[str]`**
- Returns warning messages for impossible schedules
- Empty list if no conflicts detected
- Example: `conflicts = scheduler.detect_conflicts()`

**`create_next_occurrence(task: Task) → void`**
- Creates the next instance of a recurring task
- Called internally by `Task.mark_complete()`
- Example: `scheduler.create_next_occurrence(daily_feeding_task)`

### Task Class

**`mark_complete(scheduler: Scheduler = None) → void`**
- Marks task as completed with current timestamp
- If task is recurring, creates next occurrence via scheduler
- Example: `task.mark_complete(scheduler)`

---

## Testing PawPal+

Comprehensive test coverage ensures the scheduler works correctly across all key features.

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **24 test cases** across three critical areas:

**1. Sorting Correctness (3 tests)**
- Tasks are returned in chronological order
- Empty schedules and single tasks handled correctly
- Tasks added out of order are properly sorted

**2. Recurrence Logic (4 tests)**
- Non-recurring tasks don't create next occurrences
- Daily tasks generate next occurrence exactly +1 day
- Weekly tasks generate next occurrence exactly +7 days
- New recurring tasks inherit all properties from the original

**3. Conflict Detection (7 tests)**
- No false positives (empty schedules, single tasks, completed tasks)
- Same-pet conflicts detected when a pet has multiple tasks at the same time
- Owner conflicts detected when different pets need attention simultaneously
- Both conflict types reported together when applicable
- Conflicts detected independently across multiple time slots

**4. Task Management (6 tests)**
- Task addition and scheduler tracking
- Multiple tasks for same and different pets
- Task-to-pet associations

**Status**: ✅ All 24 tests passing

---

## Troubleshooting

### Issue: Streamlit app not starting
**Solution**: Ensure Streamlit is installed (`pip install streamlit`), then run:
```bash
streamlit run app.py
```

### Issue: Conflicts not showing warnings
**Solution**: Conflicts only appear for **active (incomplete) tasks**. Make sure your conflicting tasks are marked as pending, not completed.

### Issue: Recurring task not creating next occurrence
**Solution**: 
1. Task must have `recurrence="daily"` or `recurrence="weekly"`
2. Must call `task.mark_complete(scheduler)` with scheduler reference
3. Next task appears in the full task list

### Issue: Tests failing
**Solution**: Run tests with verbose output to see which test is failing:
```bash
python -m pytest tests/test_pawpal.py -v
```

---

## Project Structure

```
ai110-module2show-pawpal-starter/
├── app.py                    # Streamlit UI application
├── pawpal_system.py          # Core system classes (Owner, Pet, Task, Scheduler)
├── main.py                   # Demo/testing script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── reflection.md             # Project reflection & learning notes
└── tests/
    └── test_pawpal.py        # Comprehensive test suite
```

---

## Future Enhancements

**Planned features** (v2.0+):
- Priority-based task rescheduling
- Duration-aware conflict detection (time windows, not just exact times)
- Travel time between pets
- Owner availability preferences
- Database persistence
- Mobile app
- Notification system

---

## License & Credits

**PawPal+** — Module 2 Project for AI110 course  
**Built**: March 2026  
**Tech Stack**: Python 3+, Streamlit, Dataclasses, pytest

---

## Support & Questions

For issues or feature requests, refer to:
- `reflection.md` — Project design decisions and trade-offs
- `pawpal_system.py` — Implementation details and docstrings
- `tests/test_pawpal.py` — Example usage in test cases
