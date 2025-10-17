#!/usr/bin/env python
"""
Master test suite runner for RequestBin
Runs all test modules and provides comprehensive report
"""

import os
import sys
import subprocess
from datetime import datetime

# Set environment for testing
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'

# Test modules to run
TEST_MODULES = [
    ('Module Imports & Core Functionality', 'test_all_modules.py'),
    ('Authentication System', 'test_auth.py'),
    ('Auto-Approve Workflow', 'test_auto_approve.py'),
    ('OTP Verification', 'test_otp.py'),
    ('Workflow & Integration', 'test_workflow.py'),
    ('WebSocket Functionality', 'test_websocket.py'),
    ('UI/UX Features', 'test_ui_features.py'),
]


def print_header(text, char="="):
    """Print a formatted header"""
    width = 70
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)


def run_test_module(name, filename):
    """Run a test module and return success status"""
    print_header(f"Running: {name}", "-")
    print(f"File: {filename}")
    print()
    
    # Get the test directory path
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(test_dir, filename)
    
    if not os.path.exists(test_file):
        print(f"⚠️  Test file not found: {test_file}")
        return None
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.dirname(test_dir),  # Run from project root
            capture_output=False,
            timeout=60
        )
        
        success = result.returncode == 0
        
        if success:
            print(f"\n✅ {name}: PASSED")
        else:
            print(f"\n❌ {name}: FAILED (exit code {result.returncode})")
        
        return success
        
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  {name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"\n❌ {name}: ERROR - {e}")
        return False


def run_quick_sanity_check():
    """Run quick sanity checks before full test suite"""
    print_header("Quick Sanity Checks", "=")
    
    checks_passed = 0
    checks_failed = 0
    
    # Check 1: Can import requestbin
    print("\n1. Checking RequestBin Enterprise import...")
    try:
        import requestbin
        print("   ✓ requestbin package imports successfully")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ Failed to import requestbin: {e}")
        checks_failed += 1
    
    # Check 2: Can import Flask app
    print("\n2. Checking Flask app...")
    try:
        from requestbin import app
        assert app is not None
        print("   ✓ Flask app initialized")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ Flask app error: {e}")
        checks_failed += 1
    
    # Check 3: Can import socketio
    print("\n3. Checking SocketIO...")
    try:
        from requestbin import socketio
        assert socketio is not None
        print("   ✓ SocketIO initialized")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ SocketIO error: {e}")
        checks_failed += 1
    
    # Check 4: Can import auth_db
    print("\n4. Checking auth storage...")
    try:
        from requestbin import auth_db
        assert auth_db is not None
        print("   ✓ Auth storage initialized")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ Auth storage error: {e}")
        checks_failed += 1
    
    # Check 5: Can import db
    print("\n5. Checking database storage...")
    try:
        from requestbin import db
        assert db is not None
        print("   ✓ Database storage initialized")
        checks_passed += 1
    except Exception as e:
        print(f"   ✗ Database storage error: {e}")
        checks_failed += 1
    
    print("\n" + "-" * 70)
    print(f"Sanity Checks: {checks_passed} passed, {checks_failed} failed")
    print("-" * 70)
    
    return checks_failed == 0


def main():
    """Run all tests and generate report"""
    start_time = datetime.now()
    
    print_header("REQUESTBIN ENTERPRISE MASTER TEST SUITE", "█")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Environment: {os.environ.get('REALM', 'unknown')}")
    print(f"Storage: {os.environ.get('STORAGE_BACKEND', 'unknown')}")
    
    # Run sanity checks first
    if not run_quick_sanity_check():
        print("\n" + "█" * 70)
        print("❌ SANITY CHECKS FAILED - STOPPING TEST SUITE")
        print("█" * 70)
        print("\nFix the basic import errors before running full test suite.")
        return 1
    
    print_header("Running Test Modules", "█")
    
    # Run all test modules
    results = []
    for name, filename in TEST_MODULES:
        result = run_test_module(name, filename)
        if result is not None:  # None means skipped
            results.append((name, result))
    
    # Calculate statistics
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    passed = sum(1 for _, success in results if success)
    failed = sum(1 for _, success in results if not success)
    total = len(results)
    
    # Print summary
    print_header("TEST SUITE SUMMARY", "█")
    
    print(f"\nCompleted at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration:.2f} seconds")
    print()
    
    print("Results by Module:")
    print("-" * 70)
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status:12} | {name}")
    
    print("\n" + "=" * 70)
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed} ({passed/total*100:.1f}%)" if total > 0 else "✅ Passed: 0")
    print(f"❌ Failed: {failed} ({failed/total*100:.1f}%)" if total > 0 else "❌ Failed: 0")
    print("=" * 70)
    
    # Final verdict
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour RequestBin Enterprise installation is fully tested and ready!")
        print("\nFeatures Verified:")
        print("  ✓ Core modules and imports")
        print("  ✓ Authentication system")
        print("  ✓ Auto-approve workflow")
        print("  ✓ OTP verification")
        print("  ✓ Bin creation and workflow")
        print("  ✓ WebSocket real-time updates")
        print("  ✓ UI/UX improvements")
        print("\nNext Steps:")
        print("  1. Run: python web.py")
        print("  2. Visit: http://localhost:4000")
        print("  3. Test all features in the browser")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print(f"\n{failed} test module(s) need attention.")
        print("Review the output above for details.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
