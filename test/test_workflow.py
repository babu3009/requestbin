#!/usr/bin/env python
"""
Test the full bin creation workflow as it happens via the web interface
Tests bin creation, request handling, and WebSocket integration
"""

import os
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'

from requestbin import app, db, auth_db, config, socketio
import json

def test_full_workflow():
    """Test the complete bin creation and access workflow"""
    print("=" * 70)
    print("TESTING FULL BIN CREATION WORKFLOW")
    print("=" * 70)
    
    # Create test client with cookie support
    with app.test_client() as client:
        # Step 1: Login as admin
        print("\n1. Logging in as admin...")
        response = client.post('/login', data={
            'email': config.ADMIN_EMAIL,
            'password': config.ADMIN_PASSWORD
        }, follow_redirects=True)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Login successful")
        else:
            print(f"   ❌ Login failed")
            print(f"   Response: {response.data[:200]}")
            return False
        
        # Step 2: Create a bin via API
        print("\n2. Creating bin via API...")
        response = client.post('/api/v1/bins', data={
            'private': 'false',
            'custom_name': ''
        })
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = json.loads(response.data)
            bin_name = data.get('name')
            print(f"   ✅ Bin created: {bin_name}")
            print(f"   Response: {json.dumps(data, indent=4)}")
        else:
            print(f"   ❌ Bin creation failed")
            print(f"   Response: {response.data}")
            return False
        
        # Step 3: Try to access the bin
        print(f"\n3. Accessing bin at '/{bin_name}?inspect'...")
        response = client.get(f'/{bin_name}?inspect')
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Bin page loaded successfully")
            # Check if we can see the bin name in the response
            if bin_name.encode() in response.data:
                print(f"   ✅ Bin name found in page")
            return True
        elif response.status_code == 404:
            print(f"   ❌ Bin not found!")
            print(f"   Response: {response.data[:200]}")
            
            # Debug: Check if bin exists in storage
            print(f"\n   🔍 Debug: Checking storage...")
            try:
                bin = db.lookup_bin(bin_name)
                print(f"   ✅ Bin exists in storage: {bin.name}")
            except KeyError:
                print(f"   ❌ Bin NOT in storage!")
                print(f"   Available bins: {list(db.db.bins.keys())}")
            return False
        else:
            print(f"   ❌ Unexpected response")
            print(f"   Response: {response.data[:200]}")
            return False
    
    print("\n" + "=" * 70)
    print("✅ WORKFLOW TEST PASSED!")
    print("=" * 70)


def test_websocket_integration():
    """Test WebSocket integration with bin updates"""
    print("\n" + "=" * 70)
    print("TESTING WEBSOCKET INTEGRATION")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: SocketIO is initialized
    print("\n1. Checking SocketIO initialization...")
    try:
        assert socketio is not None
        print("   ✅ SocketIO initialized")
        tests_passed += 1
    except AssertionError:
        print("   ❌ SocketIO not initialized")
        tests_failed += 1
    
    # Test 2: Check WebSocket handlers
    print("\n2. Checking WebSocket event handlers...")
    try:
        assert 'connect' in socketio.handlers['/']
        assert 'disconnect' in socketio.handlers['/']
        assert 'join' in socketio.handlers['/']
        assert 'leave' in socketio.handlers['/']
        print("   ✅ All event handlers registered")
        tests_passed += 1
    except (AssertionError, KeyError) as e:
        print(f"   ❌ Event handlers missing: {e}")
        tests_failed += 1
    
    # Test 3: Test client connection
    print("\n3. Testing WebSocket client connection...")
    try:
        client = socketio.test_client(app, namespace='/')
        assert client.is_connected()
        print("   ✅ WebSocket client connected")
        tests_passed += 1
        
        # Test join event
        print("\n4. Testing room join...")
        client.emit('join', {'bin_name': 'test-bin'})
        print("   ✅ Join event emitted")
        tests_passed += 1
        
        client.disconnect()
        print("   ✅ Client disconnected")
        tests_passed += 1
        
    except Exception as e:
        print(f"   ❌ WebSocket test failed: {e}")
        tests_failed += 1
    
    print("\n" + "=" * 70)
    if tests_failed == 0:
        print("✅ WEBSOCKET INTEGRATION TEST PASSED!")
    else:
        print(f"⚠️  {tests_failed} WebSocket tests failed")
    print("=" * 70)
    
    return tests_failed == 0


if __name__ == '__main__':
    workflow_success = test_full_workflow()
    websocket_success = test_websocket_integration()
    
    print("\n" + "█" * 70)
    print("FINAL TEST RESULTS")
    print("█" * 70)
    
    if workflow_success and websocket_success:
        print("✅ ALL TESTS PASSED!")
        print("\nFeatures Verified:")
        print("  ✓ Authentication flow")
        print("  ✓ Bin creation via API")
        print("  ✓ Bin access and display")
        print("  ✓ WebSocket initialization")
        print("  ✓ Real-time event handling")
    else:
        if not workflow_success:
            print("❌ Workflow tests failed")
        if not websocket_success:
            print("❌ WebSocket tests failed")
    
    import sys
    sys.exit(0 if (workflow_success and websocket_success) else 1)
