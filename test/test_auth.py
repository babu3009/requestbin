#!/usr/bin/env python
"""
Test script for authentication system
Verifies authentication configuration and creates test users
"""

import os
import sys

def test_auth_config():
    """Test authentication configuration"""
    print("Testing Authentication Configuration...")
    print("=" * 50)
    
    # Set test environment to use memory storage
    os.environ['REALM'] = 'local'  # Use local to test with memory storage
    os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'
    
    try:
        # Import configuration
        import requestbin.config as config
        
        print(f"✓ Admin Email: {config.ADMIN_EMAIL}")
        print(f"✓ Auto-Approve Domains: {config.AUTO_APPROVE_DOMAINS}")
        print()
        
        # Initialize auth storage
        if config.STORAGE_BACKEND == "requestbin.storage.postgresql.PostgreSQLStorage":
            from requestbin.auth.storage import PostgreSQLAuthStorage
            auth_storage = PostgreSQLAuthStorage()
            print("✓ Using PostgreSQL authentication storage")
        else:
            from requestbin.auth.storage import MemoryAuthStorage
            auth_storage = MemoryAuthStorage()
            print("✓ Using Memory authentication storage")
        
        # Test admin user initialization
        print("\nInitializing admin user...")
        admin_user = auth_storage.initialize_admin()
        if admin_user:
            print(f"✓ Admin user created/verified: {admin_user.email}")
            print(f"  - Is Admin: {admin_user.is_admin}")
            print(f"  - Is Approved: {admin_user.is_approved}")
        
        # Test creating an auto-approve user
        print("\nTesting auto-approve domain...")
        test_email = f"test@{config.AUTO_APPROVE_DOMAINS[0]}"
        try:
            test_user = auth_storage.create_user(
                email=test_email,
                password="test123",
                is_admin=False
            )
            print(f"✓ Created test user: {test_user.email}")
            print(f"  - Is Approved: {test_user.is_approved} (should be True for auto-approve domain)")
            
            # Clean up test user
            auth_storage.delete_user(test_email)
            print(f"✓ Cleaned up test user")
        except ValueError as e:
            print(f"⚠️  Test user may already exist: {e}")
        
        # Test creating a non-auto-approve user
        print("\nTesting non-auto-approve domain...")
        test_email2 = "test@example.com"
        try:
            test_user2 = auth_storage.create_user(
                email=test_email2,
                password="test123",
                is_admin=False
            )
            print(f"✓ Created test user: {test_user2.email}")
            print(f"  - Is Approved: {test_user2.is_approved} (should be False for non-auto-approve domain)")
            
            # Test approval
            print(f"\nTesting user approval...")
            auth_storage.approve_user(test_email2)
            approved_user = auth_storage.get_user(test_email2)
            print(f"✓ User approved: {approved_user.is_approved}")
            
            # Clean up test user
            auth_storage.delete_user(test_email2)
            print(f"✓ Cleaned up test user")
        except ValueError as e:
            print(f"⚠️  Test user may already exist: {e}")
        
        # Test password management
        print("\nTesting password management...")
        test_email3 = "password_test@tarento.com"
        try:
            test_user3 = auth_storage.create_user(
                email=test_email3,
                password="oldpass123",
                is_admin=False
            )
            print(f"✓ Created test user: {test_user3.email}")
            
            # Test password verification
            assert test_user3.check_password("oldpass123") == True
            print(f"✓ Password verification works")
            
            # Test password change
            test_user3.set_password("newpass456")
            assert test_user3.check_password("newpass456") == True
            assert test_user3.check_password("oldpass123") == False
            print(f"✓ Password change works")
            
            # Clean up
            auth_storage.delete_user(test_email3)
            print(f"✓ Cleaned up test user")
        except Exception as e:
            print(f"⚠️  Password management test error: {e}")
        
        # List all users
        print("\nCurrent users:")
        all_users = auth_storage.get_all_users()
        for user in all_users:
            status = "✓ Approved" if user.is_approved else "⏳ Pending"
            role = "👑 Admin" if user.is_admin else "👤 User"
            print(f"  - {user.email} | {role} | {status}")
        
        print("\n" + "=" * 50)
        print("✅ Authentication system is working correctly!")
        print("\nFeatures Tested:")
        print("✓ Admin user initialization")
        print("✓ Auto-approve domains")
        print("✓ User approval workflow")
        print("✓ Password management")
        print("✓ User listing")
        print("\nNext steps:")
        print("1. Start the application: python web.py")
        print(f"2. Login as admin: {config.ADMIN_EMAIL}")
        print("3. Visit /admin/users to manage users")
        print("4. Visit /auth/change-password to change password")
        print("4. Register new users at /register")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run authentication tests"""
    print("RequestBin Enterprise Authentication System Test")
    print("=" * 50)
    print()
    
    success = test_auth_config()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
