#!/usr/bin/env python3
"""Simple test runner for calculator project"""

import subprocess
import sys

def main():
    print("🚀 Running Calculator Tests...\n")
    
    # Run pytest on all tests
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
    
    if result.returncode == 0:
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        return 0
    else:
        print("\n" + "="*50)
        print("❌ SOME TESTS FAILED")
        print("="*50)
        return 1

if __name__ == "__main__":
    sys.exit(main())