#!/usr/bin/env python
"""
Apply Admin Password Change to PostgreSQL Database
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Database connection details
DB_CONFIG = {
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': int(os.environ.get('POSTGRES_PORT', '55234')),
    'database': os.environ.get('POSTGRES_DB', 'gmImNcMNjRlT'),
    'user': os.environ.get('POSTGRES_USER', 'f21e30667747'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'de9e43ee16df119956ce1db8582')
}

SCHEMA_NAME = os.environ.get('POSTGRES_SCHEMA', 'requestbin_app')

def change_admin_password():
    """Change admin user password"""
    
    print("=" * 70)
    print("RequestBin - Change Admin Password")
    print("=" * 70)
    
    # Get admin email
    admin_email = input("\nEnter admin email (default: admin@requestbin.cfapps.eu10-004.hana.ondemand.com): ").strip()
    if not admin_email:
        admin_email = "admin@requestbin.cfapps.eu10-004.hana.ondemand.com"
    
    # Get new password
    new_password = input("Enter new password: ").strip()
    if not new_password:
        print("\n❌ Error: Password cannot be empty!")
        return False
    
    # Confirm password
    confirm_password = input("Confirm new password: ").strip()
    if new_password != confirm_password:
        print("\n❌ Error: Passwords do not match!")
        return False
    
    # Import psycopg2
    try:
        import psycopg2
    except ImportError:
        print("\n❌ Error: psycopg2 not installed!")
        print("\nPlease install it with:")
        print("  pip install psycopg2-binary")
        return False
    
    # Connect to database
    print(f"\n🔌 Connecting to database at {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False
    
    # Check if user exists
    print(f"\n🔍 Checking if user '{admin_email}' exists...")
    try:
        cursor.execute(f"""
            SELECT email, is_admin, is_approved 
            FROM {SCHEMA_NAME}.users 
            WHERE email = %s
        """, (admin_email,))
        
        user = cursor.fetchone()
        
        if not user:
            print(f"\n❌ Error: User '{admin_email}' not found!")
            cursor.close()
            conn.close()
            return False
        
        print(f"✅ User found: {user[0]}")
        print(f"   Admin: {user[1]}, Approved: {user[2]}")
        
    except Exception as e:
        print(f"\n❌ Error checking user: {e}")
        cursor.close()
        conn.close()
        return False
    
    # Generate password hash
    print("\n🔐 Generating password hash...")
    password_hash = generate_password_hash(new_password)
    
    # Update password
    print(f"\n🔧 Updating password for '{admin_email}'...")
    try:
        cursor.execute(f"""
            UPDATE {SCHEMA_NAME}.users 
            SET password_hash = %s,
                updated_at = NOW()
            WHERE email = %s
        """, (password_hash, admin_email))
        
        print("✅ Password updated successfully!")
        
        # Verify the update
        cursor.execute(f"""
            SELECT email, is_admin, is_approved, updated_at
            FROM {SCHEMA_NAME}.users 
            WHERE email = %s
        """, (admin_email,))
        
        user = cursor.fetchone()
        
        print("\n" + "=" * 70)
        print("✅ Password Change Complete!")
        print("=" * 70)
        print(f"\n📧 Email:     {user[0]}")
        print(f"👤 Admin:     {user[1]}")
        print(f"✓  Approved:  {user[2]}")
        print(f"📅 Updated:   {user[3]}")
        print("\n" + "=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error updating password: {e}")
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    return True

if __name__ == '__main__':
    try:
        success = change_admin_password()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
