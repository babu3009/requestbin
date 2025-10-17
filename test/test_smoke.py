#!/usr/bin/env python
"""
Quick smoke test - verifies basic functionality
"""

import os
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'

print("=" * 70)
print("REQUESTBIN ENTERPRISE QUICK SMOKE TEST")
print("=" * 70)

tests_passed = 0
tests_failed = 0

# Test 1: Import requestbin
print("\n1. Testing requestbin import...")
try:
    import requestbin
    print("   ✅ requestbin imported")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 2: Import Flask app
print("\n2. Testing Flask app...")
try:
    from requestbin import app
    assert app is not None
    print("   ✅ Flask app initialized")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 3: Import SocketIO
print("\n3. Testing SocketIO...")
try:
    from requestbin import socketio
    assert socketio is not None
    print("   ✅ SocketIO initialized")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 4: Import database
print("\n4. Testing database...")
try:
    from requestbin import db
    assert db is not None
    print("   ✅ Database storage initialized")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 5: Import auth storage
print("\n5. Testing auth storage...")
try:
    from requestbin import auth_db
    assert auth_db is not None
    print("   ✅ Auth storage initialized")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 6: Test client
print("\n6. Testing Flask test client...")
try:
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code in [200, 302]
        print(f"   ✅ Home page accessible (status {response.status_code})")
        tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 7: Check routes
print("\n7. Testing route registration...")
try:
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/login' in routes
    assert '/logout' in routes
    assert '/auth/change-password' in routes
    assert '/' in routes
    print(f"   ✅ Routes registered ({len(routes)} total)")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Test 8: Check WebSocket
print("\n8. Testing WebSocket integration...")
try:
    assert hasattr(socketio, 'run')
    print("   ✅ WebSocket ready")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Failed: {e}")
    tests_failed += 1

# Summary
print("\n" + "=" * 70)
print(f"Results: {tests_passed} passed, {tests_failed} failed")
print("=" * 70)

if tests_failed == 0:
    print("\n✅ ALL SMOKE TESTS PASSED!")
    print("\nApplication is ready to run!")
    exit(0)
else:
    print("\n❌ SOME TESTS FAILED")
    exit(1)
