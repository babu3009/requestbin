#!/usr/bin/env python
"""
Initialize PostgreSQL schema for RequestBin
This script creates the schema and all required tables using Python (no psql needed)
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
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@requestbin.cfapps.eu10-004.hana.ondemand.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!')

def print_header(text, color='cyan'):
    colors = {
        'cyan': '\033[96m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'end': '\033[0m'
    }
    print(f"\n{colors.get(color, '')}{text}{colors['end']}")

def initialize_schema():
    """Initialize the PostgreSQL schema"""
    print("=" * 70)
    print_header("🐘 Initializing PostgreSQL Schema for RequestBin", 'green')
    print("=" * 70)
    
    print_header("\n📊 Database Connection:", 'cyan')
    print(f"   Host:     {DB_CONFIG['host']}")
    print(f"   Port:     {DB_CONFIG['port']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print(f"   User:     {DB_CONFIG['user']}")
    print(f"   Schema:   {SCHEMA_NAME}")
    
    # Try to import psycopg2
    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        print_header("\n❌ Error: psycopg2 not installed!", 'red')
        print("\nPlease install it with:")
        print("  pip install psycopg2-binary")
        return False
    
    # Connect to database
    print_header("\n🔌 Connecting to database...", 'yellow')
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Connected successfully!")
    except Exception as e:
        print_header(f"\n❌ Connection failed: {e}", 'red')
        print("\n💡 Troubleshooting:")
        print("   1. Is PostgreSQL running?")
        print("   2. Are the connection details correct?")
        print(f"   3. Does the database '{DB_CONFIG['database']}' exist?")
        return False
    
    # Read schema file
    print_header("\n📄 Reading schema.sql...", 'yellow')
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print("   ✅ Schema file loaded")
    except FileNotFoundError:
        print_header("\n❌ Error: schema.sql not found!", 'red')
        print("   Make sure you're running this from the requestbin directory")
        cursor.close()
        conn.close()
        return False
    
    # Execute schema
    print_header("\n🔧 Creating schema and tables...", 'yellow')
    try:
        cursor.execute(schema_sql)
        print("   ✅ Schema created successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
            ORDER BY table_name
        """, (SCHEMA_NAME,))
        
        tables = cursor.fetchall()
        if tables:
            print(f"\n   📋 Created {len(tables)} tables:")
            for table in tables:
                print(f"      ✓ {table[0]}")
        
        # Check if admin user was created
        cursor.execute(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.users WHERE is_admin = true
        """)
        admin_count = cursor.fetchone()[0]
        
        # Create admin user if doesn't exist or update if exists
        print(f"\n   👤 Setting up admin user: {ADMIN_EMAIL}")
        password_hash = generate_password_hash(ADMIN_PASSWORD)
        
        cursor.execute(f"""
            INSERT INTO {SCHEMA_NAME}.users 
            (email, password_hash, is_admin, is_approved, email_verified, created_at)
            VALUES (%s, %s, TRUE, TRUE, TRUE, NOW())
            ON CONFLICT (email) DO UPDATE
            SET password_hash = EXCLUDED.password_hash,
                is_admin = TRUE,
                is_approved = TRUE,
                email_verified = TRUE
        """, (ADMIN_EMAIL, password_hash))
        
        # Get updated admin count
        cursor.execute(f"""
            SELECT COUNT(*) FROM {SCHEMA_NAME}.users WHERE is_admin = true
        """)
        admin_count = cursor.fetchone()[0]
        print(f"   ✅ Admin user ready: {ADMIN_EMAIL}")
        
    except Exception as e:
        print_header(f"\n❌ Error creating schema: {e}", 'red')
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    
    # Success message
    print("\n" + "=" * 70)
    print_header("✅ PostgreSQL Schema Initialized Successfully!", 'green')
    print("=" * 70)
    
    print_header("\n📊 Database Status:", 'yellow')
    print(f"   ✓ Schema '{SCHEMA_NAME}' created")
    print(f"   ✓ {len(tables)} tables initialized")
    print(f"   ✓ {admin_count} admin user created")
    print("   ✓ Ready for connections")
    
    print_header("\n🚀 Next Step: Start the Application", 'yellow')
    print("\n   Run this command:")
    print("   .\\run-local-postgres.ps1")
    print("\n   Or manually:")
    print("   python web.py  (after setting environment variables)")
    
    print_header("\n🔑 Login Credentials:", 'yellow')
    print(f"   Email:    {ADMIN_EMAIL}")
    print(f"   Password: {ADMIN_PASSWORD}")
    
    print("\n" + "=" * 70)
    print()
    
    return True

if __name__ == '__main__':
    success = initialize_schema()
    sys.exit(0 if success else 1)
