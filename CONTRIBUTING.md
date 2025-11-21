# Contributing to PySchedule

Thank you for your interest in contributing to PySchedule! This document provides guidelines for contributing code, documentation, bug reports, and feature requests.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate in communication
- Provide constructive feedback and accept criticism gracefully
- Focus on what is best for the community and project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or derogatory comments
- Trolling, insulting/derogatory comments, or personal attacks
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers at [conduct@pyschedule.example.com]. All complaints will be reviewed and investigated promptly and fairly.

---

## Getting Started

### Ways to Contribute

**Code Contributions**:
- Implement new scheduling algorithms
- Add new scenarios to the benchmark suite
- Improve performance or add features
- Fix bugs

**Non-Code Contributions**:
- Report bugs and suggest features
- Improve documentation and tutorials
- Create examples and use cases
- Help others in discussions and issues

### Finding Good First Issues

Look for issues labeled:
- `good first issue`: Suitable for newcomers
- `help wanted`: Maintainers are seeking contributions
- `documentation`: Documentation improvements

---

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git for version control
- (Optional) Virtual environment tool (venv, conda)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyschedule.git
   cd pyschedule
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original/pyschedule.git
   ```

### Install in Development Mode

1. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install in editable mode with dev dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

   This installs:
   - PySchedule in editable mode (`-e` flag)
   - Development dependencies (pytest, black, mypy, etc.)

3. **Verify installation**:
   ```bash
   python -c "import simple_simulator; print('PySchedule installed successfully')"
   pytest tests/  # Run test suite
   ```

---

## Contribution Workflow

### 1. Create a Branch

Always create a new branch for your work:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch Naming Conventions**:
- `feature/algorithm-name`: New algorithm implementations
- `fix/issue-123`: Bug fixes (reference issue number)
- `docs/topic`: Documentation improvements
- `test/component`: Test additions or improvements

### 2. Make Changes

- Write code following [Coding Standards](#coding-standards)
- Add tests for new functionality (see [Testing Guidelines](#testing-guidelines))
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run full test suite
pytest tests/

# Run tests with coverage
pytest --cov=. --cov-report=html tests/

# Run specific test file
pytest tests/test_algorithms.py

# Run specific test
pytest tests/test_algorithms.py::TestDPEScheduler::test_dpe_alpha_parameter
```

### 4. Commit Your Changes

**Commit Message Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or modifying tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Example**:
```
feat(algorithms): implement adaptive DPE with auto-tuning

Add adaptive DPE scheduler that automatically tunes the α parameter
based on workload characteristics (burstiness, heterogeneity, deadline pressure).

Closes #42
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with the following specifics:

**Formatting**:
- Use `black` for automatic formatting
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)

**Naming Conventions**:
- Classes: `PascalCase` (e.g., `DPE_Scheduler`)
- Functions/methods: `snake_case` (e.g., `select_next_task`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_PRIORITY`)
- Private attributes: `_leading_underscore` (e.g., `_internal_state`)

**Type Hints**:
All public functions must include type hints:
```python
def select_next_task(
    self,
    available_tasks: List[Task],
    current_time: float
) -> Optional[Task]:
    """Select the next task to schedule.

    Args:
        available_tasks: List of tasks available for scheduling
        current_time: Current simulation time

    Returns:
        Selected task, or None if no task should be scheduled
    """
    pass
```

### Code Quality Tools

Run before committing:
```bash
# Auto-format code
black simple_simulator.py algorithms.py

# Check style
flake8 simple_simulator.py algorithms.py

# Type checking
mypy simple_simulator.py algorithms.py
```

---

## Testing Guidelines

### Test Structure

- Place tests in `tests/` directory
- Name test files `test_<module>.py`
- Name test classes `Test<ClassName>`
- Name test methods `test_<functionality>`

### Writing Tests

**Example Test**:
```python
import pytest
from simple_simulator import Task
from algorithms import SPT_Scheduler

class TestSPTScheduler:
    """Test suite for SPT Scheduler."""

    def test_spt_selects_shortest_task(self):
        """Test that SPT selects task with shortest processing time."""
        tasks = [
            Task(id=1, arrival_time=0.0, processing_time=10.0, priority=1, deadline=50.0),
            Task(id=2, arrival_time=0.0, processing_time=3.0, priority=1, deadline=20.0),
            Task(id=3, arrival_time=0.0, processing_time=7.0, priority=1, deadline=30.0),
        ]

        scheduler = SPT_Scheduler(tasks, num_machines=1)
        scheduler.run()

        # Task 2 (shortest) should start first
        assert tasks[1].start_time == 0.0
        assert tasks[1].completion_time == 3.0

    @pytest.mark.parametrize("num_tasks,num_machines", [
        (10, 2),
        (20, 4),
        (50, 8),
    ])
    def test_spt_completes_all_tasks(self, num_tasks, num_machines):
        """Test that SPT completes all tasks regardless of scale."""
        tasks = generate_random_tasks(num_tasks)
        scheduler = SPT_Scheduler(tasks, num_machines=num_machines)
        scheduler.run()

        # All tasks should have completion times
        assert all(task.completion_time is not None for task in tasks)
```

### Test Coverage

- Maintain **80%+ code coverage**
- All new features must include tests
- Bug fixes should include regression tests

**Check coverage**:
```bash
pytest --cov=. --cov-report=term-missing tests/
```

### Property-Based Testing

Use `hypothesis` for property-based testing when appropriate:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=1.0, max_value=100.0), min_size=1, max_size=50))
def test_spt_completion_order(processing_times):
    """Property: SPT should complete tasks in non-decreasing order of processing time."""
    tasks = [Task(id=i, arrival_time=0.0, processing_time=p, priority=1, deadline=p*2)
             for i, p in enumerate(processing_times)]

    scheduler = SPT_Scheduler(tasks, num_machines=1)
    scheduler.run()

    completion_times = sorted([(t.completion_time, t.processing_time) for t in tasks])
    # Check that shorter tasks complete before longer tasks
    assert all(completion_times[i][1] <= completion_times[i+1][1]
               for i in range(len(completion_times)-1))
```

---

## Documentation

### Docstring Format

Use **Google-style docstrings**:
```python
def calculate_deadline_pressure(task: Task, current_time: float) -> float:
    """Calculate deadline pressure for a task.

    Deadline pressure measures how close a task is to its deadline,
    ranging from 0.0 (just arrived) to 1.0 (at deadline).

    Args:
        task: Task to calculate pressure for
        current_time: Current simulation time

    Returns:
        Deadline pressure value in [0.0, 1.0]

    Raises:
        ValueError: If current_time < task.arrival_time or task.deadline <= task.arrival_time

    Examples:
        >>> task = Task(arrival_time=0.0, deadline=10.0, ...)
        >>> calculate_deadline_pressure(task, 5.0)
        0.5
    """
    if current_time < task.arrival_time:
        raise ValueError("Current time cannot be before task arrival")
    if task.deadline <= task.arrival_time:
        raise ValueError("Deadline must be after arrival time")

    return (current_time - task.arrival_time) / (task.deadline - task.arrival_time)
```

### Documentation Updates

When adding new features:
1. Update `README.md` if user-facing changes
2. Update `docs/RESEARCH.md` if theoretical contributions
3. Update `API_REFERENCE.md` for new public APIs
4. Add examples to `examples/` directory

---

## Submitting Changes

### Pull Request Process

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request** on GitHub with:
   - **Clear title** describing the change
   - **Description** explaining what and why
   - **Reference issues** (e.g., "Closes #42")
   - **Screenshots** if UI changes

4. **Address review feedback**:
   - Respond to comments
   - Make requested changes
   - Push updates to same branch (PR updates automatically)

### Pull Request Checklist

Before submitting, ensure:
- [ ] Code follows style guidelines (`black`, `flake8`, `mypy` pass)
- [ ] Tests added and passing (pytest, coverage ≥80%)
- [ ] Documentation updated
- [ ] Commit messages follow format
- [ ] Branch is up-to-date with upstream main
- [ ] No merge conflicts

### Review Process

- Maintainers will review within 1-2 weeks
- Address all feedback before merge
- At least 1 approving review required
- CI checks must pass (tests, lint, type checking)

---

## Contributing New Algorithms

### Algorithm Contribution Checklist

When implementing a new scheduling algorithm:

1. **Create algorithm class** inheriting from `SchedulerBase`:
   ```python
   from simple_simulator import SchedulerBase, Task
   from typing import List, Optional

   class MyNewScheduler(SchedulerBase):
       """Brief description of algorithm.

       Detailed explanation of scheduling policy, complexity,
       and when to use this algorithm.
       """

       def select_next_task(
           self,
           available_tasks: List[Task],
           current_time: float
       ) -> Optional[Task]:
           """Select next task according to algorithm policy."""
           # Implement your scheduling logic here
           pass
   ```

2. **Add to `algorithms.py`** or create new file `algorithms/<name>.py`

3. **Add comprehensive tests** in `tests/test_<algorithm_name>.py`

4. **Add benchmark scenarios** demonstrating strengths/weaknesses

5. **Document algorithm**:
   - Add to `docs/RESEARCH.md` (theoretical foundations)
   - Add to `README.md` (usage example)
   - Add docstrings with complexity analysis

6. **Update `runner.py`** to include algorithm in experiments

7. **Create visualizations** showing algorithm behavior

### Algorithm Evaluation

Include in your PR:
- **Performance comparison** against SPT, EDF, Priority-First, DPE
- **Complexity analysis** (time and space)
- **Use case recommendations** (when is this algorithm optimal?)
- **Parameter tuning guidance** (if algorithm has tunable parameters)

---

## Contributing Scenarios

### Scenario Contribution Guidelines

New scenarios should:
1. **Be realistic**: Based on real-world use cases or theoretical challenges
2. **Have clear purpose**: Test specific algorithm properties or trade-offs
3. **Include metadata**: Description, difficulty level, expected behavior

**Scenario Template**:
```python
def create_my_scenario():
    """Brief description of scenario.

    This scenario tests [specific property], demonstrating the trade-off
    between [metric1] and [metric2].

    Expected behavior:
    - SPT: [performance characteristics]
    - EDF: [performance characteristics]
    - DPE: [performance characteristics with optimal α]

    Difficulty: [Simple|Challenge|Extreme|Advanced]
    """
    tasks = [
        Task(id=1, arrival_time=..., processing_time=..., priority=..., deadline=...),
        # ... more tasks
    ]
    num_machines = ...

    return tasks, num_machines, "Scenario Name"
```

### Adding to Scenario Library

1. Add scenario function to `scenarios.py`
2. Add to appropriate category dictionary
3. Include in comprehensive experiment runs
4. Document expected algorithm performance

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas, announcements
- **Pull Requests**: Code review and collaboration

### Getting Help

- Check **existing issues** and **discussions** first
- Provide **minimal reproducible examples** when reporting bugs
- Include **context** (Python version, OS, PySchedule version)

### Recognition

Contributors are recognized in:
- **CONTRIBUTORS.md**: All contributors listed
- **Release notes**: Major contributions highlighted
- **GitHub contributors page**: Automatic recognition

---

## Release Process

(For maintainers)

1. Update version in `setup.py` and `simple_simulator.py`
2. Update `CHANGELOG.md` with notable changes
3. Create git tag: `git tag -a v1.x.x -m "Release v1.x.x"`
4. Push tag: `git push origin v1.x.x`
5. Create GitHub Release with changelog
6. Publish to PyPI: `python setup.py sdist bdist_wheel && twine upload dist/*`

---

## License

By contributing to PySchedule, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

## Questions?

If you have questions about contributing, feel free to:
- Open a **GitHub Discussion**
- Email the maintainers: [maintainers@pyschedule.example.com]
- Check the **FAQ** in `README.md`

Thank you for contributing to PySchedule! 🎉

---

**Version**: 1.0
**Last Updated**: 2024-11
**Maintainers**: PySchedule Development Team
