# Python Project: CLI Utilities and Algorithm Practice

## Overview
This repository contains a collection of small, focused Python programs that demonstrate core programming patterns:

- Frequency analysis using dictionaries and `collections.Counter`
- Basic string algorithm checks (anagram detection)
- Interactive command-line applications (calculator and to-do list)
- Test-driven improvements for reusable modules
- **NumPy basics for beginners (new)**

The codebase mixes learning/demo scripts and production-style, tested modules.

## New Addition: NumPy Learning Script
A new file `numpy_learning.py` has been added to help beginners understand NumPy.

### What it covers
- Creating arrays
- Array properties (shape, size, type)
- Indexing and slicing
- Mathematical operations
- Aggregation functions (sum, mean, etc.)
- Reshaping arrays
- Random number generation
- Sorting
- Combining arrays
- Boolean filtering
- Broadcasting
- Copy vs view

### Run the NumPy script
```bash
python numpy_learning.py
```

This script is designed for beginners and includes inline comments explaining each step.

## Features / Capabilities
- Dynamic calculator CLI
- Most repetitive element analysis
- To-do checklist CLI
- Algorithm demos
- NumPy beginner examples

## Project Structure
```text
python_project/
├── README.md
├── numpy_learning.py              # NumPy beginner learning script (new)
├── anagram_check.py
├── dynamic_calculator.py
├── most_frequent_element.py
├── most_repetitive.py
├── most_repetitive_element.py
├── to_do_checklist_python_list.py
└── tests/
```

## Installation
```bash
git clone https://github.com/cdasadiya/python_project.git
cd python_project
python -m venv .venv
source .venv/bin/activate
pip install -U pytest numpy
```

## Usage
Run any script using:
```bash
python filename.py
```

## Future Improvements
- Add more NumPy exercises and mini projects
- Add visualization using matplotlib
- Improve structure into learning modules

## License
No license currently defined.
