#!/usr/bin/env python
"""
Debug script to test bin creation and lookup
This helps diagnose the "Bin Not found" error
"""

import os
import sys

# Set up test environment
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'
os.environ['REALM'] = 'local'

from requestbin import db
from requestbin.models import Bin

def test_bin_creation():
    """Test creating and looking up bins"""
    print("=" * 60)
    print("TESTING BIN CREATION AND LOOKUP")
    print("=" * 60)
    
    # Test 1: Create a simple bin
    print("\n1. Creating a test bin...")
    try:
        bin1 = db.create_bin(private=False, custom_name=None)
        print(f"   ✅ Bin created: {bin1.name}")
        print(f"   - Private: {bin1.private}")
        print(f"   - Created at: {bin1.created}")
        print(f"   - Color: {bin1.color}")
    except Exception as e:
        print(f"   ❌ Error creating bin: {e}")
        return False
    
    # Test 2: Look up the bin
    print(f"\n2. Looking up bin '{bin1.name}'...")
    try:
        found_bin = db.lookup_bin(bin1.name)
        print(f"   ✅ Bin found: {found_bin.name}")
        print(f"   - Same instance: {found_bin is bin1}")
    except KeyError:
        print(f"   ❌ Bin not found!")
        print(f"   - Available bins: {list(db.db.bins.keys())}")
        return False
    except Exception as e:
        print(f"   ❌ Error looking up bin: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Create a custom named bin
    print("\n3. Creating a custom named bin...")
    try:
        bin2 = db.create_bin(private=False, custom_name="mytest")
        print(f"   ✅ Bin created: {bin2.name}")
    except Exception as e:
        print(f"   ❌ Error creating custom bin: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Look up custom bin
    print(f"\n4. Looking up custom bin 'mytest'...")
    try:
        found_bin2 = db.lookup_bin("mytest")
        print(f"   ✅ Bin found: {found_bin2.name}")
    except KeyError:
        print(f"   ❌ Bin not found!")
        print(f"   - Available bins: {list(db.db.bins.keys())}")
        return False
    except Exception as e:
        print(f"   ❌ Error looking up custom bin: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: List all bins
    print(f"\n5. Current bins in storage:")
    print(f"   Total bins: {db.count_bins()}")
    for name in db.db.bins.keys():
        print(f"   - {name}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_bin_creation()
    sys.exit(0 if success else 1)
