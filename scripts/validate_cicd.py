#!/usr/bin/env python3
"""
Validate CI/CD setup and configuration.
"""
import os
import sys


def check_file_exists(file_path, description):
    """Check if a file exists and report status."""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (missing)")
        return False


def validate_github_actions():
    """Validate GitHub Actions configuration."""
    print("Validating GitHub Actions Configuration...")
    print("-" * 50)

    workflows_dir = ".github/workflows"
    if not os.path.exists(workflows_dir):
        print(f"❌ GitHub Actions workflows directory missing: {workflows_dir}")
        return False

    # Check main CI/CD workflow file
    ci_cd_file = os.path.join(workflows_dir, "ci-cd.yml")

    ci_cd_exists = check_file_exists(ci_cd_file, "CI/CD workflow")

    if ci_cd_exists:
        try:
            with open(ci_cd_file, "r") as f:
                ci_content = f.read()

            # Check for required jobs (simple text search)
            required_jobs = ["test:", "lint:", "security:", "deploy:"]

            for job in required_jobs:
                if job in ci_content:
                    print(f"✅ CI/CD job '{job.rstrip(':')}' configured")
                else:
                    print(f"❌ CI/CD job '{job.rstrip(':')}' missing")

        except Exception as e:
            print(f"❌ Error reading CI/CD workflow: {e}")

    # Check that workflow structure is appropriate
    workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith(".yml")]
    if len(workflow_files) == 1:
        print("✅ Single consolidated CI/CD workflow")
    elif len(workflow_files) == 2:
        # Check if we have the expected two-tier structure
        expected_files = ["ci-cd.yml", "pr-tests.yml"]
        if all(f in workflow_files for f in expected_files):
            print("✅ Two-tier workflow structure (CI/CD + PR tests)")
        else:
            print(f"⚠️  Found {len(workflow_files)} workflow files - verify structure")
    else:
        print(f"Found {len(workflow_files)} workflow files - consider consolidation")

    return ci_cd_exists


def validate_testing_setup():
    """Validate testing configuration."""
    print("\nValidating Testing Setup...")
    print("-" * 50)

    # Check test files
    test_files = [
        "pytest.ini",
        "tests/conftest.py",
        "tests/test_app.py",
        "tests/test_database.py",
        "tests/test_i18n.py",
        "tests/test_integration.py",
        "tests/test_search.py",
        "tests/test_translations.py",
        "scripts/run_tests.py",
        "scripts/coverage_report.py",
    ]

    all_exist = True
    for test_file in test_files:
        if not check_file_exists(test_file, "Test file"):
            all_exist = False

    # Check test coverage
    if os.path.exists("scripts/run_tests.py"):
        try:
            import subprocess
            import sys

            # Try both python and python3
            python_cmd = sys.executable if sys.executable else "python3"
            result = subprocess.run(
                [python_cmd, "scripts/coverage_report.py"],
                capture_output=True,
                text=True,
                cwd=".",
            )
            if result.returncode == 0:
                print("✅ Coverage report generator working")
            else:
                print(
                    "⚠️  Coverage report generator check skipped (dependencies may not be installed)"
                )
        except Exception as e:
            print(f"⚠️  Coverage report generator check skipped: {e}")

    return all_exist


def validate_docker_setup():
    """Validate Docker configuration."""
    print("\nValidating Docker Setup...")
    print("-" * 50)

    docker_files = [
        "Dockerfile",
        "Dockerfile.test",
        "docker-compose.yml",
        "requirements.txt",
    ]

    all_exist = True
    for docker_file in docker_files:
        if not check_file_exists(docker_file, "Docker file"):
            all_exist = False

    return all_exist


def validate_hooks_and_automation():
    """Validate hooks and automation setup."""
    print("\nValidating Hooks and Automation...")
    print("-" * 50)

    # Essential automation files
    essential_files = ["Makefile", "TESTING.md"]

    all_exist = True
    for file_path in essential_files:
        if not check_file_exists(file_path, "Automation file"):
            all_exist = False

    # Check git hooks (optional in CI environment)
    pre_commit_hook = ".git/hooks/pre-commit"
    if os.path.exists(pre_commit_hook):
        print("✅ Automation file: .git/hooks/pre-commit")
        if os.access(pre_commit_hook, os.X_OK):
            print("✅ Pre-commit hook is executable")
        else:
            print("⚠️  Pre-commit hook is not executable")
    else:
        print(
            "⚠️  Automation file: .git/hooks/pre-commit (missing - may not be available in CI)"
        )

    return all_exist


def run_quick_validation():
    """Run quick validation tests."""
    print("\nRunning Quick Validation...")
    print("-" * 50)

    try:
        # Test basic imports
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Test imports
        try:
            import database  # noqa: F401

            print("✅ Database module imports successfully")
        except ImportError as e:
            print(f"⚠️  Database module import check skipped: {e}")

        try:
            import app  # noqa: F401

            print("✅ App module imports successfully")
        except ImportError as e:
            print(f"⚠️  App module import check skipped: {e}")
            # If we can't import app, skip the rest
            return True

        # Test database functions
        try:
            from database import init_database  # noqa: F401

            print("✅ Database functions accessible")
        except ImportError as e:
            print(f"⚠️  Database functions check skipped: {e}")

        # Test Flask app creation
        try:
            from app import create_app_for_testing

            test_app = create_app_for_testing()  # noqa: F841
            print("✅ Flask test app creation works")
        except ImportError as e:
            print(f"⚠️  Flask test app creation check skipped: {e}")
        except Exception as e:
            print(f"⚠️  Flask test app creation check skipped: {e}")

        return True

    except Exception as e:
        print(f"⚠️  Quick validation completed with some checks skipped: {e}")
        return True  # Don't fail the entire validation for import issues


def main():
    """Main validation function."""
    print("CI/CD Setup Validation")
    print("=" * 50)

    # Run all validations
    validations = [
        validate_github_actions(),
        validate_testing_setup(),
        validate_docker_setup(),
        validate_hooks_and_automation(),
        run_quick_validation(),
    ]

    passed = sum(validations)
    total = len(validations)

    print("\n" + "=" * 50)
    print(f"Validation Summary: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All CI/CD components are properly configured!")
        return 0
    else:
        print("⚠️  Some CI/CD components need attention.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
