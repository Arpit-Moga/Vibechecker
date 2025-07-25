import pytest
import unittest
import sys
import os

def run_pytest():
    # Run all pytest-based test files
    pytest_args = [
        os.path.join(os.path.dirname(__file__), "agent_tests.py"),
        os.path.join(os.path.dirname(__file__), "endpoint_tests.py"),
        os.path.join(os.path.dirname(__file__), "orchestration_tests.py"),
        os.path.join(os.path.dirname(__file__), "schema_tests.py"),
        os.path.join(os.path.dirname(__file__), "validation_tests.py"),
    ]
    print("Running pytest tests...")
    result = pytest.main(pytest_args)
    print("pytest result code:", result)
    return result

def run_unittest():
    # Run workflow_tests.py (unittest-based)
    print("Running unittest workflow tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern="workflow_tests.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("unittest result:", result)
    return result

def main():
    pytest_result = run_pytest()
    unittest_result = run_unittest()
    if pytest_result == 0 and unittest_result.wasSuccessful():
        print("\nAll tests PASSED.")
        sys.exit(0)
    else:
        print("\nSome tests FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
