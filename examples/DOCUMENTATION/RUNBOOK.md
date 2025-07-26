# RUNBOOK: Python Examples Collection

## 1. Purpose
This runbook provides essential information and instructions for operating and understanding the collection of Python example scripts. It covers setup, execution, and common operational considerations for `example1.py`, `example2.py`, and `example3.py`.

## 2. System Overview
This repository contains three independent Python scripts, each demonstrating different programming concepts:

*   **`example1.py`**: Contains a `greet` function demonstrating basic function calls, string manipulation, and handling various input types (integers, `None`, lists). It includes a `main` function to showcase its usage.
*   **`example2.py`**: Implements a `Calc` class with methods for basic arithmetic operations (addition, subtraction, multiplication, division). This script demonstrates object-oriented programming concepts.
*   **`example3.py`**: Processes a list of employee data, calculating total earnings based on hours worked, including overtime. It also demonstrates robust error handling using `try-except-finally` blocks for `ZeroDivisionError` and `IndexError`.

## 3. Prerequisites
To run these scripts, you need:
*   **Python 3.x**: An installed Python interpreter. It is recommended to use Python 3.6 or newer.

## 4. Setup and Installation
No specific installation steps are required beyond having Python installed. Simply ensure the `.py` files are accessible on your system.

## 5. Usage Instructions

### 5.1. Running `example1.py`
This script demonstrates a `greet` function with various inputs.

**To execute:**
```bash
python example1.py
```

**Expected Output:**
The script will print greeting messages to the console, demonstrating how the `greet` function handles different data types passed as arguments. You will observe output for integer, `None`, and list inputs.

### 5.2. Running `example2.py`
This script defines a `Calc` class for basic arithmetic operations. To use it, you would typically import the class into another script or interact with it in an interactive Python session.

**Example Interactive Usage:**
```python
# Start a Python interactive session
python

# Inside the Python interpreter:
from example2 import Calc

calculator = Calc()
print(f"5 + 3 = {calculator.add(5, 3)}")
print(f"10 - 4 = {calculator.sub(10, 4)}")
print(f"6 * 7 = {calculator.mul(6, 7)}")
print(f"20 / 5 = {calculator.div(20, 5)}")
```

**Expected Output (from interactive usage):**
```
5 + 3 = 8
10 - 4 = 6
6 * 7 = 42
20 / 5 = 4.0
```

### 5.3. Running `example3.py`
This script processes employee data and demonstrates error handling.

**To execute:**
```bash
python example3.py
```

**Expected Output:**
The script will iterate through the `employees` list, calculate total earnings for each, and print the results. It will also demonstrate its error handling by catching and reporting `ZeroDivisionError` and `IndexError` if such conditions were to occur (though the provided data does not trigger them, the `try-except` blocks are active).

## 6. Troubleshooting

*   **`ModuleNotFoundError`**: If you encounter this when trying to import `Calc` from `example2.py`, ensure you are running the Python interpreter from the directory containing `example2.py` or that the file is in your Python path.
*   **`TypeError` in `example1.py`**: The `greet` function in `example1.py` is designed to handle various types, but unexpected types might lead to runtime errors or unexpected string concatenations. Review the `greet` function's logic if output is not as expected.
*   **`ZeroDivisionError` in `example2.py`**: If you call `calculator.div(a, 0)`, a `ZeroDivisionError` will occur. The `Calc` class does not include internal handling for this specific case.
*   **`ZeroDivisionError` or `IndexError` in `example3.py`**: While `example3.py` includes `try-except` blocks to handle these errors gracefully, if you modify the `employees` data in a way that causes these errors, the script will print an error message to the console instead of crashing.

## 7. Maintenance and Operations

*   **Code Review**: Periodically review the scripts for potential improvements, bug fixes, or to update them with newer Python features.
*   **Data Integrity**: For `example3.py`, ensure the `employees` data structure remains consistent (e.g., each employee entry is a list of three elements: name, age, hours) to prevent `IndexError`.
*   **Dependency Management**: As these are simple scripts with no external dependencies, no specific dependency management is required beyond ensuring a compatible Python version is installed.