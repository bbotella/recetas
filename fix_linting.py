#!/usr/bin/env python3
"""
Script to run linting checks locally and fix common issues
"""

import subprocess
import sys
import os
import tempfile


def run_command(cmd, description=""):
    """Run a command and return its result"""
    print(f"\n🔍 {description}")
    print(f"Running: {cmd}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Return code: {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def install_linting_tools():
    """Install linting tools"""
    print("📦 Installing linting tools...")

    tools = [
        "pip install --user flake8",
        "pip install --user black",
        "pip install --user pylint",
        "pip install --user bandit",
        "pip install --user safety",
    ]

    for tool in tools:
        print(f"Installing: {tool}")
        subprocess.run(tool, shell=True)


def run_basic_python_check():
    """Run basic Python syntax check"""
    print("\n🐍 Running basic Python syntax check...")

    python_files = ["app.py", "database.py", "run_tests.py", "coverage_report.py"]

    for file in python_files:
        if os.path.exists(file):
            result = run_command(f"python3 -m py_compile {file}", f"Checking {file}")
            if not result:
                print(f"❌ Syntax error in {file}")
                return False

    print("✅ All Python files have valid syntax")
    return True


def run_flake8_check():
    """Run flake8 linting"""
    print("\n🔧 Running Flake8 check...")

    # Try to run flake8 with user installation
    flake8_cmd = "python3 -m flake8 --max-line-length=88 --extend-ignore=E203,W503 *.py"
    return run_command(flake8_cmd, "Running Flake8")


def run_black_check():
    """Run black formatting check"""
    print("\n🎨 Running Black formatting check...")

    black_cmd = "python3 -m black --check --diff *.py"
    return run_command(black_cmd, "Running Black check")


def run_black_format():
    """Run black formatting"""
    print("\n🎨 Running Black formatting...")

    black_cmd = "python3 -m black *.py"
    return run_command(black_cmd, "Running Black formatting")


def run_pylint_check():
    """Run pylint check"""
    print("\n🔍 Running Pylint check...")

    pylint_cmd = "python3 -m pylint --disable=all --enable=unused-import,undefined-variable,syntax-error *.py"
    return run_command(pylint_cmd, "Running Pylint")


def create_setup_cfg():
    """Create basic setup.cfg for linting configuration"""
    setup_cfg_content = """[flake8]
max-line-length = 88
extend-ignore = E203,W503,F401
exclude =
    venv,
    __pycache__,
    .git,
    .pytest_cache,
    htmlcov,
    build,
    dist,
    *.egg-info

[pycodestyle]
max-line-length = 88
ignore = E203,W503

[pydocstyle]
ignore = D100,D101,D102,D103,D104,D105,D106,D107,D203,D213,D413
"""

    with open("setup.cfg", "w") as f:
        f.write(setup_cfg_content)

    print("✅ Created setup.cfg with linting configuration")


def fix_common_issues():
    """Fix common linting issues in files"""
    print("\n🔧 Fixing common linting issues...")

    # List of files to check and fix
    files_to_fix = [
        "add_all_valencian_translations.py",
        "add_valencian_translations_part1.py",
        "enhance_valencian_translations.py",
        "verify_valencian_translations.py",
    ]

    for file in files_to_fix:
        if os.path.exists(file):
            print(f"Checking {file}...")

            # Read file content
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic fixes
            original_content = content

            # Fix imports organization
            lines = content.split("\n")
            new_lines = []
            imports_section = []
            in_imports = False

            for line in lines:
                if line.startswith("import ") or line.startswith("from "):
                    imports_section.append(line)
                    in_imports = True
                elif in_imports and line.strip() == "":
                    # End of imports section
                    in_imports = False
                    # Sort imports
                    imports_section.sort()
                    new_lines.extend(imports_section)
                    new_lines.append(line)
                    imports_section = []
                else:
                    new_lines.append(line)

            # Write back if changes were made
            new_content = "\n".join(new_lines)
            if new_content != original_content:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ Fixed imports in {file}")


def main():
    """Main function to run all linting checks"""
    print("🔍 Running linting checks and fixes...")
    print("=" * 60)

    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ Please run this script from the project root directory")
        return False

    # Create linting configuration
    create_setup_cfg()

    # Try to install linting tools
    install_linting_tools()

    # Run basic Python check
    if not run_basic_python_check():
        print("❌ Basic Python syntax check failed")
        return False

    # Fix common issues
    fix_common_issues()

    # Run Black formatting
    print("\n🎨 Attempting to format code with Black...")
    run_black_format()

    # Run linting checks
    results = []

    # Flake8 check
    results.append(("Flake8", run_flake8_check()))

    # Black check
    results.append(("Black", run_black_check()))

    # Pylint check
    results.append(("Pylint", run_pylint_check()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 LINTING RESULTS SUMMARY")
    print("=" * 60)

    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 All linting checks passed!")
        return True
    else:
        print("\n⚠️  Some linting checks failed. Please review the output above.")
        print("💡 You may need to manually fix some issues.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
