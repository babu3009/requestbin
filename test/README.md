# RequestBin Enterprise Test Suite

# RequestBin Enterprise Test Suite

This directory contains comprehensive test scripts for the RequestBin Enterprise application with PostgreSQL backend, authentication, WebSocket support, and UI/UX improvements.

## Quick Start

Run all tests:
```bash
python test/run_all_tests.py
```

Or with conda environment:
```powershell
conda activate requestbin
python test/run_all_tests.py
```

## Test Modules

### 1. **run_all_tests.py** - Master Test Runner
Runs all test modules sequentially and provides comprehensive report.
- Quick sanity checks
- Module-by-module execution
- Summary statistics
- Pass/fail reporting

**Usage:**
```bash
python test/run_all_tests.py
```

### 2. **test_all_modules.py** - Core Module Tests
Tests all module imports and core functionality.
- Package imports (requestbin.*, requestbin.auth.*, requestbin.views.*, etc.)
- User class and password hashing
- Auto-approve logic
- Memory storage operations
- Flask forms (LoginForm, RegistrationForm)
- Route registration

**Usage:**
```bash
python test/test_all_modules.py
```

### 3. **test_auth.py** - Authentication System Tests
Tests the complete authentication system.
- Admin user initialization
- Auto-approve domains
- User approval workflow
- Password management
- User listing

**Usage:**
```bash
python test/test_auth.py
```

### 4. **test_auto_approve.py** - Auto-Approve Tests
Tests domain-based auto-approval functionality.

**Usage:**
```bash
python test/test_auto_approve.py
```

### 5. **test_otp.py** - OTP Verification Tests
Tests email verification with OTP codes.

**Usage:**
```bash
python test/test_otp.py
```

### 6. **test_workflow.py** - Integration Workflow Tests
Tests complete bin creation and access workflow.
- User login
- Bin creation via API
- Bin page access
- WebSocket integration
- Event handler registration
- Client connection testing

**Usage:**
```bash
python test/test_workflow.py
```

### 7. **test_websocket.py** - WebSocket Tests
Tests real-time WebSocket/SocketIO functionality.
- SocketIO initialization
- Event handler registration
- Client-side code verification
- Server-side event emission
- Dependencies check

**Features Tested:**
- Real-time bin updates
- Room-based event emission
- Auto-refresh on new requests
- Bidirectional communication

**Usage:**
```bash
python test/test_websocket.py
```

### 8. **test_ui_features.py** - UI/UX Feature Tests
Tests layout updates, copy functionality, and navigation improvements.
- Dropdown menu improvements (Home link, About icon)
- Bin URL conditional display
- Bin URL bar positioning
- Copy button functionality
- CSS styling verification
- Password management routes

**Features Tested:**
- Layout template improvements
- Copy to clipboard functionality
- Professional CSS styling
- Navigation enhancements

**Usage:**
```bash
python test/test_ui_features.py
```

### 9. **test_inspect_view.py** - Inspect View Tests
Tests the bin inspect view functionality.

**Usage:**
```bash
python test/test_inspect_view.py
```

### 10. **test_postgresql_config.py** - PostgreSQL Config Tests
Tests PostgreSQL configuration and connection.

**Usage:**
```bash
python test/test_postgresql_config.py
```

### 11. **test_schema_config.py** - Schema Configuration Tests
Tests database schema configuration.

**Usage:**
```bash
python test/test_schema_config.py
```

### 12. **test_sap_btp_config.py** - SAP BTP Config Tests
Tests SAP BTP deployment configuration.

**Usage:**
```bash
python test/test_sap_btp_config.py
```

## Test Environment Setup

### Environment Variables
Tests use memory storage by default:
```python
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'memory'
```

To test with PostgreSQL:
```python
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.postgresql.PostgreSQLStorage'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_PORT'] = '55234'
# ... other PostgreSQL settings
```

### Dependencies
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

Key testing requirements:
- Flask >= 3.1.2
- flask-socketio
- simple-websocket
- flask-login
- flask-wtf
- psycopg2-binary (for PostgreSQL tests)

## Test Coverage

### Module Coverage
- ✅ Core modules (config, models, util, filters)
- ✅ Storage backends (memory, postgresql, redis)
- ✅ Authentication (auth.models, auth.storage, auth.forms, auth.utils)
- ✅ Views (main, api, auth)
- ✅ Database (db wrapper)
- ✅ WebSocket (socketio, event handlers)

### Functionality Coverage
- ✅ User creation and management
- ✅ Password hashing and verification
- ✅ Auto-approve logic
- ✅ Admin initialization
- ✅ User approval workflow
- ✅ Bin creation and access
- ✅ Request handling
- ✅ Real-time updates via WebSocket
- ✅ UI/UX improvements
- ✅ Copy to clipboard
- ✅ Password management routes

### Route Coverage
- ✅ Authentication routes (/login, /logout, /register, /profile)
- ✅ Admin routes (/admin/users, /admin/approve, /admin/reject)
- ✅ Password routes (/auth/change-password, /auth/forgot-password, /auth/reset-password)
- ✅ API routes (/api/v1/bins, /api/v1/bins/<name>, etc.)
- ✅ Main routes (/, /<bin>, /docs, /about)
- ✅ Email verification routes (/verify-email, /resend-otp)

## Continuous Integration

For CI/CD pipelines:
```bash
# Run all tests and exit with appropriate code
python test/run_all_tests.py
echo $?  # 0 = success, 1 = failure
```

## Troubleshooting

### Import Errors
If you see module import errors:
1. Ensure you're in the project root directory
2. Activate the correct conda environment: `conda activate requestbin`
3. Verify PYTHONPATH includes the project root

### Database Connection Errors
For PostgreSQL tests:
1. Ensure PostgreSQL is running
2. Verify connection parameters in environment variables
3. Check schema exists: `requestbin_app`

### WebSocket Test Failures
If WebSocket tests fail:
1. Ensure flask-socketio is installed: `pip install flask-socketio`
2. Check simple-websocket is installed: `pip install simple-websocket`
3. Verify socketio initialization in requestbin/__init__.py

## Writing New Tests

Template for new test modules:
```python
#!/usr/bin/env python
"""
Test description
"""

import os
import sys

# Set environment
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'memory'

def test_feature():
    """Test a specific feature"""
    print("Testing feature...")
    # Your test code here
    return True  # or False

def main():
    """Run all tests"""
    success = test_feature()
    
    if success:
        print("✅ ALL TESTS PASSED!")
        return 0
    else:
        print("❌ TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Test Results Interpretation

### Exit Codes
- **0**: All tests passed
- **1**: One or more tests failed
- **130**: Tests interrupted by user (Ctrl+C)

### Common Success Output
```
█████████████████████████████████████████████████████████████████████
                    FINAL RESULTS
█████████████████████████████████████████████████████████████████████

Total Tests: 8
✅ Passed: 8 (100.0%)
❌ Failed: 0 (0.0%)

🎉 ALL TESTS PASSED! 🎉
```

### Common Failure Patterns
- **Import Errors**: Missing dependencies or incorrect PYTHONPATH
- **Connection Errors**: Database not running or wrong credentials
- **Assertion Errors**: Code logic doesn't match expected behavior
- **Timeout Errors**: Tests taking too long (> 60 seconds)

## Support

For issues or questions:
1. Check test output for specific error messages
2. Review individual test module documentation above
3. Verify environment setup and dependencies
4. Check application logs in development mode

## Test Files

### Python Test Scripts

#### Core Functionality Tests
- **test_all_modules.py** - Comprehensive test suite for all modules
- **test_workflow.py** - End-to-end workflow integration tests

#### Authentication & Security Tests
- **test_auth.py** - Authentication system tests
  - User registration and login
  - Password hashing and verification
  - Session management
- **test_otp.py** - OTP (One-Time Password) verification tests
  - OTP generation and validation
  - OTP expiration handling
  - Email verification workflow
- **test_auto_approve.py** - Auto-approval functionality tests
  - Domain-based auto-approval
  - User approval workflow

#### Database & Configuration Tests
- **test_postgresql_config.py** - PostgreSQL configuration tests
  - Database connection testing
  - Schema validation
  - Configuration parsing
- **test_schema_config.py** - Database schema tests
  - Schema creation and migration
  - Table structure validation
  - Index verification
- **test_sap_btp_config.py** - SAP BTP configuration tests
  - VCAP_SERVICES parsing
  - Service binding validation
  - Environment configuration

#### UI/UX Tests
- **test_inspect_view.py** - Inspect view functionality tests
  - Split-panel interface
  - Request display and formatting
  - cURL command generation

### Shell Scripts

- **test-app.ps1** - PowerShell script for application testing
  - Automated application startup
  - Health check verification
  - Environment setup

- **test-inspect-view.bat** - Batch script for inspect view testing
  - Quick inspect view validation
  - Manual testing helper

## Running Tests

### Run All Tests

```bash
# From project root
python -m pytest test/

# Or using the comprehensive test script
python test/test_all_modules.py
```

### Run Specific Test Files

```bash
# Authentication tests
python test/test_auth.py

# OTP verification tests
python test/test_otp.py

# Database configuration tests
python test/test_postgresql_config.py

# Inspect view tests
python test/test_inspect_view.py

# Workflow tests
python test/test_workflow.py
```

### Run PowerShell Test Script

```powershell
# From project root
.\test\test-app.ps1
```

### Run Batch Test Script

```cmd
# From project root
.\test\test-inspect-view.bat
```

## Test Requirements

### Python Dependencies

Ensure all testing dependencies are installed:

```bash
pip install pytest pytest-cov flask-testing
```

### Environment Setup

Tests require the following environment variables:

```bash
# Storage backend
STORAGE_BACKEND=requestbin.storage.memory.MemoryStorage

# Authentication
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=testpassword
AUTO_APPROVE_DOMAINS=example.com,test.com

# Session
FLASK_SESSION_SECRET_KEY=test-secret-key

# Application settings
MAX_REQUESTS=200
REALM=test
```

### Database Setup (for PostgreSQL tests)

PostgreSQL tests require a running PostgreSQL instance:

```bash
# Set PostgreSQL connection details
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=test_db
export POSTGRES_USER=test_user
export POSTGRES_PASSWORD=test_password
export POSTGRES_SCHEMA=requestbin_test
```

## Test Coverage

To run tests with coverage reporting:

```bash
# Run with coverage
python -m pytest test/ --cov=requestbin --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Example configurations:

### GitHub Actions

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install pytest pytest-cov
    python -m pytest test/ --cov=requestbin
```

### GitLab CI

```yaml
test:
  script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - python -m pytest test/ --cov=requestbin
```

## Test Results

Test results and reports are documented in:
- [TEST_RESULTS.md](../docs/TEST_RESULTS.md) - Overall test results
- [TEST_INSPECT_VIEW.md](../docs/TEST_INSPECT_VIEW.md) - Inspect view test details

## Writing New Tests

When adding new tests, follow these conventions:

1. **Naming**: Use `test_` prefix for test files and test functions
2. **Location**: Place tests in this `test/` directory
3. **Structure**: Group related tests in the same file
4. **Documentation**: Add docstrings explaining test purpose
5. **Isolation**: Ensure tests don't depend on external state
6. **Cleanup**: Clean up any resources created during tests

### Example Test Structure

```python
"""
Test module for [feature name]
Tests [feature description]
"""

import pytest
from requestbin import app, config

def test_feature_basic():
    """Test basic functionality of [feature]"""
    # Arrange
    expected = "value"
    
    # Act
    result = some_function()
    
    # Assert
    assert result == expected

def test_feature_edge_case():
    """Test edge case for [feature]"""
    # Test implementation
    pass
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure requestbin module is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Database Connection Errors**
```bash
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check connection string
echo $POSTGRES_HOST $POSTGRES_PORT $POSTGRES_DB
```

**Environment Variable Issues**
```bash
# Use .env file for local testing
cp .env.example .env
# Edit .env with your settings
```

## Related Documentation

- [Testing Results](../docs/TEST_RESULTS.md)
- [Inspect View Testing](../docs/TEST_INSPECT_VIEW.md)
- [Authentication Implementation](../docs/AUTH_IMPLEMENTATION.md)
- [PostgreSQL Setup](../docs/POSTGRESQL_SETUP.md)
