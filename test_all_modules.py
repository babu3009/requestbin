#!/usr/bin/env python
"""
Comprehensive module test for RequestBin with Authentication
Tests all modules individually
"""

import os
import sys

# Set environment for testing
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'memory'

def test_module_imports():
    """Test all module imports"""
    print("=" * 60)
    print("MODULE IMPORT TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Core modules
    print("\n1. Core Modules:")
    try:
        import requestbin.config as config
        print("  ✓ requestbin.config")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.config - {e}")
        tests_failed += 1
    
    try:
        import requestbin.models
        print("  ✓ requestbin.models")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.models - {e}")
        tests_failed += 1
    
    try:
        import requestbin.util
        print("  ✓ requestbin.util")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.util - {e}")
        tests_failed += 1
    
    try:
        import requestbin.filters
        print("  ✓ requestbin.filters")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.filters - {e}")
        tests_failed += 1
    
    # Test 2: Storage modules
    print("\n2. Storage Modules:")
    try:
        import requestbin.storage.memory
        print("  ✓ requestbin.storage.memory")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.storage.memory - {e}")
        tests_failed += 1
    
    try:
        import requestbin.storage.postgresql
        print("  ✓ requestbin.storage.postgresql")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.storage.postgresql - {e}")
        tests_failed += 1
    
    try:
        import requestbin.storage.redis
        print("  ✓ requestbin.storage.redis")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.storage.redis - {e}")
        tests_failed += 1
    
    # Test 3: Authentication modules
    print("\n3. Authentication Modules:")
    try:
        import requestbin.auth
        print("  ✓ requestbin.auth")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.auth - {e}")
        tests_failed += 1
    
    try:
        import requestbin.auth_storage
        print("  ✓ requestbin.auth_storage")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.auth_storage - {e}")
        tests_failed += 1
    
    try:
        import requestbin.forms
        print("  ✓ requestbin.forms")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.forms - {e}")
        tests_failed += 1
    
    try:
        import requestbin.auth_views
        print("  ✓ requestbin.auth_views")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.auth_views - {e}")
        tests_failed += 1
    
    # Test 4: Flask application modules
    print("\n4. Flask Application Modules:")
    try:
        from requestbin import app
        print("  ✓ requestbin.app (Flask application)")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.app - {e}")
        tests_failed += 1
    
    try:
        from requestbin import auth_db
        print("  ✓ requestbin.auth_db (Auth storage)")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.auth_db - {e}")
        tests_failed += 1
    
    try:
        import requestbin.api
        print("  ✓ requestbin.api")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.api - {e}")
        tests_failed += 1
    
    try:
        import requestbin.views
        print("  ✓ requestbin.views")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.views - {e}")
        tests_failed += 1
    
    try:
        import requestbin.db
        print("  ✓ requestbin.db")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ requestbin.db - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_functionality():
    """Test core functionality"""
    print("\n" + "=" * 60)
    print("FUNCTIONALITY TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test User class
    print("\n1. User Class:")
    try:
        from requestbin.auth import User
        user = User(email="test@example.com", is_admin=False)
        user.set_password("password123")
        
        assert user.email == "test@example.com"
        assert user.is_admin == False
        assert user.check_password("password123") == True
        assert user.check_password("wrongpass") == False
        
        print("  ✓ User creation")
        print("  ✓ Password hashing")
        print("  ✓ Password verification")
        tests_passed += 3
    except Exception as e:
        print(f"  ✗ User class tests - {e}")
        tests_failed += 1
    
    # Test Auto-approval
    print("\n2. Auto-Approval Logic:")
    try:
        from requestbin.auth import User
        import requestbin.config as config
        
        user1 = User(email="test@tarento.com")
        user2 = User(email="test@example.com")
        
        assert user1.should_auto_approve() == True
        assert user2.should_auto_approve() == False
        
        print("  ✓ Auto-approve for @tarento.com")
        print("  ✓ Manual approve for other domains")
        tests_passed += 2
    except Exception as e:
        print(f"  ✗ Auto-approval tests - {e}")
        tests_failed += 1
    
    # Test Memory Storage
    print("\n3. Memory Storage:")
    try:
        from requestbin.auth_storage import MemoryAuthStorage
        storage = MemoryAuthStorage()
        
        # Create user
        user = storage.create_user("test@tarento.com", "pass123", is_admin=False)
        assert user.is_approved == True  # Auto-approved
        
        # Get user
        retrieved = storage.get_user("test@tarento.com")
        assert retrieved.email == "test@tarento.com"
        
        # Check password
        assert retrieved.check_password("pass123") == True
        
        # Delete user
        storage.delete_user("test@tarento.com")
        assert storage.get_user("test@tarento.com") == None
        
        print("  ✓ Create user")
        print("  ✓ Retrieve user")
        print("  ✓ Password verification")
        print("  ✓ Delete user")
        tests_passed += 4
    except Exception as e:
        print(f"  ✗ Memory storage tests - {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Test Forms
    print("\n4. Flask Forms:")
    try:
        from requestbin.forms import LoginForm, RegistrationForm
        from requestbin import app
        
        with app.test_request_context():
            login_form = LoginForm()
            reg_form = RegistrationForm()
            
            assert login_form is not None
            assert reg_form is not None
            assert hasattr(login_form, 'email')
            assert hasattr(login_form, 'password')
            assert hasattr(reg_form, 'email')
            assert hasattr(reg_form, 'password')
            assert hasattr(reg_form, 'password2')
        
        print("  ✓ LoginForm")
        print("  ✓ RegistrationForm")
        print("  ✓ Form fields")
        tests_passed += 3
    except Exception as e:
        print(f"  ✗ Form tests - {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Test Flask Routes
    print("\n5. Flask Routes:")
    try:
        from requestbin import app
        
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        # Check auth routes exist
        assert '/login' in routes
        assert '/logout' in routes
        assert '/register' in routes
        assert '/profile' in routes
        assert '/admin/users' in routes
        
        print("  ✓ /login")
        print("  ✓ /logout")
        print("  ✓ /register")
        print("  ✓ /profile")
        print("  ✓ /admin/users")
        tests_passed += 5
    except Exception as e:
        print(f"  ✗ Route tests - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def main():
    """Run all tests"""
    print("\n" + "█" * 60)
    print("REQUESTBIN COMPREHENSIVE MODULE TESTS")
    print("█" * 60)
    
    import_success = test_module_imports()
    functionality_success = test_functionality()
    
    print("\n" + "█" * 60)
    print("FINAL RESULTS")
    print("█" * 60)
    
    if import_success and functionality_success:
        print("✅ ALL TESTS PASSED!")
        print("\nYour RequestBin installation is ready to use!")
        print("\nNext steps:")
        print("  1. Run: python web.py")
        print("  2. Visit: http://localhost:4000")
        print("  3. Login: admin@requestbin.local / admin123")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease review the errors above and fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
