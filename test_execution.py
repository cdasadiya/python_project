#!/usr/bin/env python3
"""
Comprehensive test script to execute all Python files in the repository.
This script tests each file individually and reports success/failure.
"""

import subprocess
import sys
from pathlib import Path

# List of all Python files to test
TEST_FILES = [
    "anagram_check.py",
    "datetime_master_utility.py",
    "dynamic_calculator.py",
    "most_frequent_element.py",
    "most_repetitive.py",
    "most_repetitive_element.py",
    "numpy_learning.py",
    "oop_learning_hospital_system.py",
    "pandas_methods_demo.py",
    "pydantic_validation_demo.py",
    "streamlit_calculator.py",
    "to_do_checklist_python_list.py",
    "webscraping_learning_framework.py",
]

def run_file_with_stdin(filepath, test_input=""):
    """Execute a Python file with provided stdin input."""
    try:
        result = subprocess.run(
            [sys.executable, str(filepath)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)

def main():
    repo_root = Path(__file__).parent
    results = {}
    
    print("=" * 80)
    print("PYTHON FILES EXECUTION TEST")
    print("=" * 80)
    
    for filename in TEST_FILES:
        filepath = repo_root / filename
        
        if not filepath.exists():
            results[filename] = ("SKIP", "File not found")
            print(f"\n❌ {filename}: File not found")
            continue
        
        print(f"\n🧪 Testing: {filename}")
        print("-" * 80)
        
        # Provide minimal input for interactive scripts
        if "calculator" in filename:
            test_input = "5\n"  # Exit
        elif "to_do" in filename:
            test_input = "7\n"  # Exit
        elif "datetime" in filename:
            test_input = "0\n"  # Exit
        elif "most_repetitive_element" in filename:
            test_input = "1,2,2,3\n"  # Input data
        elif "webscraping" in filename:
            test_input = "0\n"  # Exit
        elif "oop_learning" in filename:
            test_input = "3\n"  # Exit
        else:
            test_input = ""
        
        returncode, stdout, stderr = run_file_with_stdin(filepath, test_input)
        
        if returncode == 0:
            results[filename] = ("PASS", stdout[:200])
            print(f"✅ PASS - File executed successfully")
            if stdout:
                print(f"Output (first 200 chars): {stdout[:200]}")
        elif returncode == -1 and "TIMEOUT" in stderr:
            results[filename] = ("TIMEOUT", stderr)
            print(f"⏱️  TIMEOUT - File took too long to execute")
        else:
            results[filename] = ("FAIL", stderr[:200])
            print(f"❌ FAIL - Return code: {returncode}")
            if stderr:
                print(f"Error (first 200 chars): {stderr[:200]}")
    
    # Summary Report
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    
    summary = {"PASS": 0, "FAIL": 0, "TIMEOUT": 0, "SKIP": 0}
    
    for filename, (status, output) in results.items():
        summary[status] = summary.get(status, 0) + 1
        status_symbol = {"PASS": "✅", "FAIL": "❌", "TIMEOUT": "⏱️", "SKIP": "⊘"}[status]
        print(f"{status_symbol} {filename:40} [{status}]")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(TEST_FILES)} files")
    print(f"✅ PASSED:  {summary['PASS']}")
    print(f"❌ FAILED:  {summary['FAIL']}")
    print(f"⏱️  TIMEOUT: {summary['TIMEOUT']}")
    print(f"⊘ SKIPPED: {summary['SKIP']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
