# TESTING

This document outlines the testing strategy and guidelines for the project. Comprehensive testing is crucial to ensure the reliability, correctness, and maintainability of our codebase.

## 1. Testing Philosophy

We aim to maintain a robust suite of tests, primarily focusing on:

*   **Unit Tests**: To verify the smallest testable parts of an application (e.g., individual functions, methods, or classes) work as expected in isolation.
*   **Integration Tests**: (Future consideration) To ensure that different modules or services used together function correctly.

## 2. Test Framework

We use [pytest](https://docs.pytest.org/en/stable/) as our primary testing framework due to its simplicity, powerful features, and extensive plugin ecosystem.

## 3. Setting Up the Test Environment

To run tests, you need to have `pytest` installed. It's recommended to do this within a virtual environment.

1.  **Create a virtual environment (if you haven't already):**
    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
3.  **Install pytest:**
    ```bash
    pip install pytest
    ```

## 4. Running Tests

Once `pytest` is installed and your virtual environment is active, you can run tests from the project root directory.

*   **Run all tests:**
    ```bash
    pytest
    ```
*   **Run tests in a specific file:**
    ```bash
    pytest tests/test_example1.py
    ```
*   **Run a specific test function:**
    ```bash
    pytest tests/test_example2.py::test_add_positive_numbers
    ```

## 5. Test Directory Structure

All test files should reside in a `tests/` directory at the root of the project. Test files should be named following the `test_*.py` or `*_test.py` convention, and test functions within them should start with `test_`.

```
project_root/
├── example1.py
├── example2.py
├── example3.py
└── tests/
    ├── test_example1.py
    ├── test_example2.py
    └── test_example3.py
```

## 6. Writing New Tests

When adding new features or fixing bugs, always write corresponding tests. Here are guidelines for writing tests for the existing modules:

### 6.1. `example1.py` Tests

Focus on the `greet` function. Consider various input types and expected behaviors.

*   **Valid Inputs**: Test with standard string names.
*   **Edge Cases/Invalid Inputs**: Test with `None`, numbers, lists, or other non-string types to observe how the function handles them (e.g., does it raise an error, or does it print unexpected output?).
*   **Loop Behavior**: While direct testing of `print` calls can be tricky, you can mock `print` or ensure the loop iterates the correct number of times if the function returned a value.

**Example `tests/test_example1.py` snippet:**

```python
import pytest
from example1 import greet

def test_greet_with_string_name(capsys):
    greet("Alice")
    captured = capsys.readouterr()
    assert "Hello Alice" in captured.out
    assert "Hello Alice0" in captured.out # Check for name modification

def test_greet_with_none_input(capsys):
    greet(None)
    captured = capsys.readouterr()
    assert "Hello None" in captured.out
    # Add more assertions based on expected behavior for None

def test_greet_with_list_input(capsys):
    greet([1, 2, 3])
    captured = capsys.readouterr()
    assert "Hello [1, 2, 3]" in captured.out
    # Add more assertions based on expected behavior for list
```

### 6.2. `example2.py` Tests

Focus on the `Calc` class methods (`add`, `sub`, `mul`, `div`).

*   **Basic Operations**: Test with positive and negative integers, and floating-point numbers.
*   **Zero**: Test addition/subtraction/multiplication with zero.
*   **Division by Zero**: Ensure the `div` method handles division by zero gracefully (e.g., raises a `ZeroDivisionError`).
*   **Edge Cases**: Large numbers, very small numbers.

**Example `tests/test_example2.py` snippet:**

```python
import pytest
from example2 import Calc

@pytest.fixture
def calculator():
    return Calc()

def test_add_positive_numbers(calculator):
    assert calculator.add(2, 3) == 5

def test_sub_negative_result(calculator):
    assert calculator.sub(5, 10) == -5

def test_mul_by_zero(calculator):
    assert calculator.mul(7, 0) == 0

def test_div_by_positive(calculator):
    assert calculator.div(10, 2) == 5.0

def test_div_by_zero_raises_error(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.div(10, 0)
```

### 6.3. `example3.py` Tests

Focus on the logic for calculating `total` based on employee data.

*   **Age <= 40**: Test with employees whose age is 40 or less.
*   **Age > 40**: Test with employees whose age is greater than 40, ensuring the overtime calculation is correct.
*   **Edge Cases**: Employees with negative age (as seen in the example data), zero age, zero `emp[2]` (which seems to be a rate or hours).
*   **Data Integrity**: Consider if the input `employees` list can contain malformed data (e.g., not enough elements in a sublist).

**Example `tests/test_example3.py` snippet:**

```python
import pytest
# Assuming the calculation logic is extracted into a function or class for testability
# For now, we'll assume we're testing the script's output or a refactored function.

# If the calculation logic is in a function, e.g., calculate_employee_total(age, rate):
# from example3 import calculate_employee_total

# def test_employee_total_under_40():
#     assert calculate_employee_total(30, 10) == 30 * 10

# def test_employee_total_over_40():
#     assert calculate_employee_total(45, 10) == (40 * 10) + (5 * 10 * 1.5)

# def test_employee_total_at_40():
#     assert calculate_employee_total(40, 10) == 40 * 10

# def test_employee_total_negative_age():
#     # Define expected behavior for negative age, e.g., raise ValueError or return 0
#     # with pytest.raises(ValueError):
#     #     calculate_employee_total(-5, 10)
#     pass # Placeholder if direct testing of script output is needed
```

## 7. Continuous Integration (CI)

(Future consideration) Once a robust test suite is in place, consider integrating tests into a CI pipeline (e.g., GitHub Actions, GitLab CI, Jenkins). This will automatically run tests on every code push, ensuring that new changes don't introduce regressions.