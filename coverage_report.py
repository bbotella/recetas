#!/usr/bin/env python3
"""
Coverage analysis for the testing suite.
"""
import os
import sys
import ast
import glob
from pathlib import Path

def analyze_function_coverage(file_path):
    """Analyze function coverage in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'lineno': node.lineno,
                    'is_test': node.name.startswith('test_')
                })
        
        return functions
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return []

def get_tested_functions():
    """Get all functions that have tests."""
    tested_functions = set()
    
    test_files = glob.glob('tests/test_*.py')
    for test_file in test_files:
        functions = analyze_function_coverage(test_file)
        for func in functions:
            if func['is_test']:
                # Extract the function being tested from test name
                test_name = func['name']
                if test_name.startswith('test_'):
                    tested_function = test_name[5:]  # Remove 'test_' prefix
                    tested_functions.add(tested_function)
    
    return tested_functions

def analyze_source_files():
    """Analyze source files for function coverage."""
    source_files = ['app.py', 'database.py']
    coverage_report = {}
    
    for file_path in source_files:
        if os.path.exists(file_path):
            functions = analyze_function_coverage(file_path)
            coverage_report[file_path] = {
                'functions': functions,
                'total_functions': len([f for f in functions if not f['name'].startswith('_')])
            }
    
    return coverage_report

def generate_coverage_report():
    """Generate a coverage report."""
    print("Coverage Analysis Report")
    print("=" * 50)
    
    # Analyze source files
    coverage_report = analyze_source_files()
    tested_functions = get_tested_functions()
    
    total_functions = 0
    tested_count = 0
    
    for file_path, data in coverage_report.items():
        print(f"\n{file_path}:")
        print("-" * 30)
        
        file_functions = 0
        file_tested = 0
        
        for func in data['functions']:
            if not func['name'].startswith('_'):  # Skip private functions
                file_functions += 1
                is_tested = any(tested_func in func['name'] for tested_func in tested_functions)
                
                status = "✓" if is_tested else "✗"
                print(f"  {status} {func['name']} (line {func['lineno']})")
                
                if is_tested:
                    file_tested += 1
        
        file_coverage = (file_tested / file_functions * 100) if file_functions > 0 else 0
        print(f"  Coverage: {file_tested}/{file_functions} ({file_coverage:.1f}%)")
        
        total_functions += file_functions
        tested_count += file_tested
    
    # Overall coverage
    overall_coverage = (tested_count / total_functions * 100) if total_functions > 0 else 0
    
    print("\n" + "=" * 50)
    print(f"Overall Coverage: {tested_count}/{total_functions} ({overall_coverage:.1f}%)")
    
    # Test files summary
    print(f"\nTest Files:")
    test_files = glob.glob('tests/test_*.py')
    for test_file in test_files:
        functions = analyze_function_coverage(test_file)
        test_count = len([f for f in functions if f['is_test']])
        print(f"  {test_file}: {test_count} tests")
    
    return overall_coverage

def main():
    """Main function."""
    if not os.path.exists('tests'):
        print("No tests directory found!")
        sys.exit(1)
    
    coverage = generate_coverage_report()
    
    print(f"\n{'='*50}")
    print("Testing Infrastructure Status:")
    print(f"✓ pytest configuration: {'pytest.ini' if os.path.exists('pytest.ini') else 'Missing'}")
    print(f"✓ Test fixtures: {'conftest.py' if os.path.exists('tests/conftest.py') else 'Missing'}")
    print(f"✓ Requirements: {'requirements.txt' if os.path.exists('requirements.txt') else 'Missing'}")
    print(f"✓ Coverage reporting: {coverage:.1f}%")
    
    if coverage >= 80:
        print("\n🎉 Excellent test coverage!")
    elif coverage >= 60:
        print("\n👍 Good test coverage!")
    elif coverage >= 40:
        print("\n⚠️  Moderate test coverage - consider adding more tests")
    else:
        print("\n❌ Low test coverage - more tests needed")

if __name__ == "__main__":
    main()