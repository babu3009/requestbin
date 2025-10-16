#!/usr/bin/env python
"""
Test the full bin creation workflow as it happens via the web interface
"""

import os
os.environ['REALM'] = 'local'

from requestbin import app, db, auth_db, config
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

if __name__ == '__main__':
    success = test_full_workflow()
    
    if not success:
        print("\n💡 The 'Bin Not found' error is reproduced!")
        print("   This suggests an issue with the request flow or sessions.")
    
    import sys
    sys.exit(0 if success else 1)
