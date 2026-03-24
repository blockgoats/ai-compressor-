#!/usr/bin/env python3
"""
Test runner for Ramanujan Compression SDK

This script runs all tests and provides a comprehensive test report.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_tests(test_type="all", verbose=False, coverage=False):
    """Run tests with specified options."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    if coverage:
        cmd.extend(["--cov=ramanujan_compression", "--cov=ramanujan_tokenizer", "--cov-report=html"])
    
    # Add test type filters
    if test_type == "unit":
        cmd.extend(["tests/test_compressor.py", "tests/test_tokenizer.py"])
    elif test_type == "integration":
        cmd.extend(["tests/test_integration.py"])
    elif test_type == "pro":
        cmd.extend(["-m", "pro"])
    elif test_type == "gpu":
        cmd.extend(["-m", "gpu"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    else:  # all
        cmd.append("tests/")
    
    print(f"Running tests: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_examples():
    """Run example scripts to verify they work."""
    print("Running examples...")
    print("-" * 50)
    
    examples_dir = Path(__file__).parent / "examples"
    if not examples_dir.exists():
        print("No examples directory found")
        return True
    
    example_files = list(examples_dir.glob("*.py"))
    if not example_files:
        print("No example files found")
        return True
    
    success = True
    for example_file in example_files:
        print(f"Running {example_file.name}...")
        try:
            result = subprocess.run([sys.executable, str(example_file)], 
                                  capture_output=True, text=True, cwd=Path(__file__).parent)
            if result.returncode == 0:
                print(f"✓ {example_file.name} completed successfully")
            else:
                print(f"✗ {example_file.name} failed:")
                print(result.stderr)
                success = False
        except Exception as e:
            print(f"✗ {example_file.name} failed with exception: {e}")
            success = False
    
    return success

def check_imports():
    """Check if all modules can be imported."""
    print("Checking imports...")
    print("-" * 50)
    
    modules_to_check = [
        "ramanujan_compression",
        "ramanujan_compression.compressor",
        "ramanujan_compression.utils",
        "ramanujan_tokenizer",
        "ramanujan_tokenizer.tokenization_ramanujan",
        "ramanujan_tokenizer.config",
    ]
    
    success = True
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            success = False
        except Exception as e:
            print(f"✗ {module}: {e}")
            success = False
    
    return success

def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run Ramanujan Compression SDK tests")
    parser.add_argument("--type", choices=["all", "unit", "integration", "pro", "gpu", "fast"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")
    parser.add_argument("--examples", "-e", action="store_true", help="Run examples")
    parser.add_argument("--imports", "-i", action="store_true", help="Check imports")
    parser.add_argument("--all", "-a", action="store_true", help="Run all checks")
    
    args = parser.parse_args()
    
    print("Ramanujan Compression SDK - Test Runner")
    print("=" * 50)
    
    success = True
    
    # Check imports
    if args.imports or args.all:
        success &= check_imports()
        print()
    
    # Run tests
    if not args.examples and not args.imports:
        success &= run_tests(args.type, args.verbose, args.coverage)
        print()
    
    # Run examples
    if args.examples or args.all:
        success &= run_examples()
        print()
    
    # Summary
    print("=" * 50)
    if success:
        print("✓ All checks passed!")
        return 0
    else:
        print("✗ Some checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())