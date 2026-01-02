
#!/usr/bin/env python3
"""Test runner for calculator project"""

import subprocess
import sys
import os

def run_unit_tests():
    """Run unit tests"""
    print("\n" + "="*50)
    print("Running Unit Tests")
    print("="*50)
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_unit.py", "-v"])
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests"""
    print("\n" + "="*50)
    print("Running Integration Tests")
    print("="*50)
    result = subprocess.run([sys.executable, "tests/test_integration.py"])
    return result.returncode == 0

def run_coverage():
    """Run tests with coverage report"""
    print("\n" + "="*50)
    print("Generating Coverage Report")
    print("="*50)
    subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=Calculator",
        "--cov-report=html",
        "--cov-report=term",
        "tests/"
    ])

def main():
    """Main test runner"""
    print("Starting Calculator Test Suite...")
    
    all_passed = True
    
    # Run unit tests
    if not run_unit_tests():
        all_passed = False
    
    # Run integration tests
    if not run_integration_tests():
        all_passed = False
    
    # Generate coverage report
    run_coverage()
    
    # Final result
    print("\n" + "="*50)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())