#!/usr/bin/env python
"""
Create admin user for RequestBin
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
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@requestbin.local')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!')

def create_admin_user():
    """Create or update admin user"""
    print("=" * 70)
    print("\n🔑 Creating Admin User for RequestBin\n")
    print("=" * 70)
    
    print(f"\nAdmin Email: {ADMIN_EMAIL}")
    print(f"Schema: {SCHEMA_NAME}")
    print(f"Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    # Try to import psycopg2
    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        print("\n❌ Error: psycopg2 not installed!")
        print("\nPlease install it with:")
        print("  pip install psycopg2-binary")
        return False
    
    # Connect to database
    print("\n🔌 Connecting to database...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        return False
    
    # Hash the password
    password_hash = generate_password_hash(ADMIN_PASSWORD)
    
    # Check if user exists
    print(f"\n🔍 Checking if user '{ADMIN_EMAIL}' exists...")
    try:
        cursor.execute(f"""
            SELECT email, is_admin, is_approved 
            FROM {SCHEMA_NAME}.users 
            WHERE email = %s
        """, (ADMIN_EMAIL,))
        
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"✅ User exists: {existing_user[0]}")
            print(f"   Admin: {existing_user[1]}, Approved: {existing_user[2]}")
            
            # Update user to be admin
            print(f"\n🔧 Updating user to admin with new password...")
            cursor.execute(f"""
                UPDATE {SCHEMA_NAME}.users 
                SET password_hash = %s,
                    is_admin = TRUE,
                    is_approved = TRUE
                WHERE email = %s
            """, (password_hash, ADMIN_EMAIL))
            print("✅ User updated successfully!")
        else:
            print(f"❌ User does not exist. Creating new user...")
            
            # Create new admin user
            cursor.execute(f"""
                INSERT INTO {SCHEMA_NAME}.users 
                (email, password_hash, is_admin, is_approved, created_at)
                VALUES (%s, %s, TRUE, TRUE, NOW())
            """, (ADMIN_EMAIL, password_hash))
            print("✅ Admin user created successfully!")
        
        # Verify the user
        cursor.execute(f"""
            SELECT email, is_admin, is_approved, created_at
            FROM {SCHEMA_NAME}.users 
            WHERE email = %s
        """, (ADMIN_EMAIL,))
        
        user = cursor.fetchone()
        print("\n" + "=" * 70)
        print("\n✅ Admin User Ready!")
        print("\n" + "=" * 70)
        print(f"\n📧 Email:     {user[0]}")
        print(f"🔑 Password:  {ADMIN_PASSWORD}")
        print(f"👤 Admin:     {user[1]}")
        print(f"✓  Approved:  {user[2]}")
        print(f"📅 Created:   {user[3]}")
        print("\n" + "=" * 70)
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    return True

if __name__ == '__main__':
    success = create_admin_user()
    sys.exit(0 if success else 1)
