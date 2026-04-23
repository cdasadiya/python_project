# Python Project: CLI Utilities and Algorithm Practice

## Overview
This repository contains a collection of small, focused Python programs that demonstrate core programming patterns:

- Frequency analysis using dictionaries and `collections.Counter`
- Basic string algorithm checks (anagram detection)
- Interactive command-line applications (calculator and to-do list)
- Test-driven improvements for reusable modules

The codebase mixes **learning/demo scripts** and **production-style, tested modules**. The main maintained components are the dynamic calculator, most repetitive element utilities, and to-do checklist workflow.

## Features / Capabilities
- **Dynamic calculator CLI** with add, subtract, multiply, divide, menu navigation, and safe divide-by-zero handling.
- **Most repetitive element analysis**:
  - Unique mode detection
  - Tie handling via custom exception (`NoModeError`)
  - Helper to return all tied top-frequency elements
  - CSV numeric parsing for interactive input
- **To-do checklist CLI**:
  - Add and remove tasks
  - Mark tasks as complete/incomplete
  - Summarize outcomes
  - Demonstrate common Python list operations (`extend`, `insert`, `sort`, `reverse`, `count`, `index`)
- **Algorithm demos** for:
  - Anagram checking using dictionaries
  - Alternative frequency-count implementations
- **Automated tests** for key modules using `pytest`.

## Project Structure
```text
python_project/
├── README.md
├── anagram_check.py                     # Standalone anagram demo script
├── dynamic_calculator.py                # Calculator module + interactive CLI
├── most_frequent_element.py             # Dictionary frequency demo (verbose)
├── most_repetitive.py                   # Simple frequency demo script
├── most_repetitive_element.py           # Reusable mode-analysis utilities + CLI
├── to_do_checklist_python_list.py       # To-do CLI with list operations
└── tests/
    ├── test_dynamic_calculator.py       # Unit tests for calculator functions/CLI flow
    ├── test_most_repetitive_element.py  # Unit tests for mode/parsing logic
    └── test_todo.py                     # Unit tests for to-do behaviors
```

## Installation
### Prerequisites
- Python **3.10+** (recommended)
- `pip`

### Setup
```bash
# 1) Clone repository
git clone https://github.com/cdasadiya/python_project.git
cd python_project

# 2) (Optional but recommended) create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3) Install test dependency
pip install -U pytest
```

## Usage Instructions
### 1) Run the dynamic calculator
```bash
python dynamic_calculator.py
```
Example flow:
- Choose operation (`1` to `4`)
- Enter two numeric values
- Read computed result
- Choose `5` to exit

### 2) Run most repetitive element finder (interactive)
```bash
python most_repetitive_element.py
```
Example input:
```text
1,2,2,3,2,3,4,5
```
Expected output includes the unique most repetitive element, or tie information when applicable.

### 3) Run to-do checklist app
```bash
python to_do_checklist_python_list.py
```
You can view tasks, add/remove tasks, mark completion status, run list-operations demo, and print a summary.

### 4) Run algorithm demo scripts
```bash
python anagram_check.py
python most_repetitive.py
python most_frequent_element.py
```

### 5) Run tests
```bash
pytest -q
```

## Code Flow / Architecture
This is a script-first repository organized around independent modules:

1. **User interaction layer (CLI loops)**
   - `run_calculator()` and `menu()` expose command-line menus.
   - `run_interactive()` handles input for frequency analysis.

2. **Core business logic functions**
   - Arithmetic operations (`add`, `subtract`, `multiply`, `divide`)
   - Frequency computation and mode selection (`most_repetitive_element`, `all_most_repetitive_elements`)
   - Input normalization/parsing (`get_number`, `parse_csv_numbers`)
   - To-do state transition functions (`add_task`, `remove_task`, `mark_tasks`)

3. **Error handling strategy**
   - Built-in exceptions (`ValueError`, `ZeroDivisionError`) for invalid user input
   - Domain-specific exception (`NoModeError`) for no unique mode

4. **Testing strategy**
   - `pytest` covers normal flows, validation errors, and interactive paths via monkeypatching `input` and capturing printed output.

## Key Modules Explanation
### `dynamic_calculator.py`
- Provides arithmetic operations as pure functions.
- Wraps numeric input parsing in `get_number()` with retry logic.
- Uses dispatch table (`operations` dictionary) to map menu options to functions.

### `most_repetitive_element.py`
- Uses `Counter` for concise, reliable frequency analysis.
- Enforces a strict unique-mode contract in `most_repetitive_element()`.
- Provides fallback `all_most_repetitive_elements()` when ties should be retained.
- Includes CSV parsing utility (`parse_csv_numbers`) that supports ints/floats and validates malformed input.

### `to_do_checklist_python_list.py`
- Maintains in-memory checklist state via module-level lists.
- Implements basic CRUD-like task operations plus completion classification.
- Includes an “advanced operations” section intended for Python list API practice.

### Demo scripts
- `anagram_check.py`, `most_repetitive.py`, and `most_frequent_element.py` are educational, print-based examples that are not currently structured as reusable modules.

## Dependencies
### Runtime
- Python standard library only for main scripts (`collections`, `typing`, etc.)

### Development / Testing
- `pytest`

Suggested `requirements-dev.txt` content:
```text
pytest>=7.0
```

## Future Improvements
Based on current implementation, the following improvements would make the project more production-ready:

- Add a `requirements.txt` / `pyproject.toml` for explicit dependency management.
- Refactor module-level mutable state in to-do app into a class-based design for easier testing and reuse.
- Introduce a shared CLI framework (`argparse`, `typer`, or `click`) to standardize command interfaces.
- Add linting and formatting automation (e.g., Ruff + Black + pre-commit).
- Add CI workflow (GitHub Actions) for automated tests on pull requests.
- Consolidate duplicate demo scripts and remove redundancy in frequency-analysis examples.
- Add type-checking (`mypy` or pyright) and stricter annotations.
- Add package structure (`src/`) and entry points for installation as a command-line tool.

## Contribution Guidelines
Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feat/your-change
   ```
3. Make changes with tests.
4. Run checks:
   ```bash
   pytest -q
   ```
5. Commit with clear messages.
6. Open a pull request describing purpose, implementation details, and test results.

Recommended practices:
- Keep functions small and single-purpose.
- Prefer pure functions for core logic.
- Include/adjust tests for behavior changes.
- Preserve backward compatibility for CLI prompts when possible.

## License
A license file is not currently present.

For open-source distribution, consider adding an MIT License (`LICENSE` file) unless your organization requires a different license model.
