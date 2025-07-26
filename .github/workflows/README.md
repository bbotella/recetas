# GitHub Actions Workflows Configuration

## Overview

This project uses a two-tier GitHub Actions workflow system to optimize CI/CD performance and provide appropriate feedback for different scenarios.

## Workflow Structure

### 1. Pull Request Tests (`.github/workflows/pr-tests.yml`)

**Trigger:** Pull requests to main/master/develop branches

**Purpose:** Provide fast feedback to contributors without running expensive deployment operations

**Jobs:**
- **test**: Runs comprehensive test suite on Python 3.9, 3.10, 3.11
- **lint**: Code style and formatting checks (BLOCKING - must pass)
- **security**: Security vulnerability scanning (non-blocking)
- **validate**: CI/CD setup validation and app startup test
- **pr-summary**: Generates summary report for PR review

**Features:**
- ✅ Matrix testing across Python versions
- ✅ Fast feedback loop (no deployment)
- ✅ Comprehensive test coverage
- ✅ Security scanning
- ✅ Automated PR summary generation
- ✅ Non-blocking linting (informational only)

### 2. CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Trigger:** Push to main/master/develop branches

**Purpose:** Full CI/CD pipeline with testing, validation, and deployment

**Jobs:**
- **test**: Same as PR tests but runs on actual pushes
- **lint**: Code quality checks (BLOCKING - must pass)
- **security**: Security vulnerability scanning (non-blocking)
- **deploy**: Docker build, test, and push to registry (main/master only)

**Features:**
- ✅ Full deployment pipeline
- ✅ Multi-platform Docker builds (amd64, arm64)
- ✅ Docker Hub integration
- ✅ Container testing before deployment
- ✅ Quality gates (deploy only after tests pass)

## Workflow Triggers

```yaml
# PR Tests - Runs on:
pull_request:
  branches: [ main, master, develop ]
  types: [ opened, synchronize, reopened ]

# CI/CD Pipeline - Runs on:
push:
  branches: [ main, master, develop ]
```

## Quality Gates

### Pull Request Requirements
- ✅ All tests must pass across Python versions
- ⚠️ Linting issues are blocking (must be fixed)
- ⚠️ Security issues are flagged but non-blocking
- ✅ Application must start successfully

### Deployment Requirements
- ✅ All tests must pass
- ✅ All lint checks must pass
- ✅ Docker container must build successfully
- ✅ Container health check must pass
- ✅ Only deploys from main/master branch

## Benefits

### For Contributors
- **Fast Feedback**: Quick test results on PRs
- **Clear Status**: Automated PR summary with next steps
- **Quality Control**: Linting issues must be fixed before merge
- **Comprehensive**: Tests across multiple Python versions

### For Maintainers
- **Quality Assurance**: Thorough testing before merge
- **Automated Deployment**: Push to main triggers deployment
- **Security Monitoring**: Automated vulnerability scanning
- **Consistent Environment**: Docker ensures consistent deployments

## Usage

### Creating a Pull Request
1. Create your feature branch
2. Push changes to your fork
3. Open a Pull Request
4. Wait for PR Tests workflow to complete
5. Review automated summary and fix any issues
6. Request review from maintainers

### Merging to Main
1. PR Tests must pass
2. Code review approved
3. Merge to main branch
4. CI/CD Pipeline automatically runs
5. If all tests pass, deploys to production

## Monitoring

### GitHub Actions Interface
- View workflow runs in the "Actions" tab
- Check test results and logs
- Download security scan reports
- Monitor deployment status

### PR Status Checks
- Test results appear as status checks on PRs
- Automated summary in PR conversation
- Links to detailed logs and reports

## Configuration

### Environment Variables
- `DATABASE_PATH`: Path to test database
- `FLASK_ENV`: Flask environment (testing/development)
- `FLASK_PORT`: Port for application testing

### Secrets Required
- `DOCKER_HUB_ACCESS_TOKEN`: For Docker Hub deployment
- `CODECOV_TOKEN`: For coverage reporting (optional)

## Troubleshooting

### Common Issues

**Tests Failing:**
- Check test logs in GitHub Actions
- Run `python run_tests.py` locally
- Ensure all dependencies are installed

**Linting Issues:**
- Run `black .` for formatting
- Run `flake8 .` for style check
- Run `pylint --disable=all --enable=unused-import,undefined-variable,syntax-error *.py` for analysis
- Issues are blocking and must be fixed

**Security Issues:**
- Review Bandit report artifacts
- Run `safety check` locally
- Issues are flagged but won't block PR

**Docker Build Issues:**
- Check Dockerfile syntax
- Ensure all dependencies are in requirements.txt
- Test build locally with `docker build .`

## Future Enhancements

- [ ] Add end-to-end testing
- [ ] Implement performance benchmarks
- [ ] Add automated changelog generation
- [ ] Integrate with external monitoring tools
- [ ] Add notification integrations (Slack, Discord)