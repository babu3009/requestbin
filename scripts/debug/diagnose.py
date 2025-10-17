#!/usr/bin/env python
"""
Comprehensive diagnostic for RequestBin
Checks configuration, database connectivity, and authentication
"""

import os
import sys

print("=" * 70)
print("REQUESTBIN DIAGNOSTIC TOOL")
print("=" * 70)

# Check 1: Environment Variables
print("\n📋 ENVIRONMENT VARIABLES:")
print("-" * 70)
env_vars = [
    'STORAGE_BACKEND', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB',
    'POSTGRES_USER', 'POSTGRES_SCHEMA', 'POSTGRES_PASSWORD',
    'AUTO_APPROVE_DOMAINS', 'ADMIN_EMAIL', 'SMTP_HOST', 'REALM'
]
for var in env_vars:
    value = os.environ.get(var, '<not set>')
    if 'PASSWORD' in var and value != '<not set>':
        value = '<set but hidden>'
    print(f"  {var:25} = {value}")

# Check 2: Load Configuration
print("\n⚙️  LOADED CONFIGURATION:")
print("-" * 70)
try:
    from requestbin import config
    print(f"  STORAGE_BACKEND:        {config.STORAGE_BACKEND}")
    print(f"  REALM:                  {config.REALM}")
    print(f"  MAX_REQUESTS:           {config.MAX_REQUESTS}")
    print(f"  BIN_TTL:                {config.BIN_TTL} seconds ({config.BIN_TTL//3600} hours)")
    print(f"  AUTO_APPROVE_DOMAINS:   {config.AUTO_APPROVE_DOMAINS}")
    print(f"  ADMIN_EMAIL:            {config.ADMIN_EMAIL}")
    
    if 'postgresql' in config.STORAGE_BACKEND.lower():
        print(f"\n  PostgreSQL Configuration:")
        print(f"    HOST:                 {config.POSTGRES_HOST}")
        print(f"    PORT:                 {config.POSTGRES_PORT}")
        print(f"    DB:                   {config.POSTGRES_DB}")
        print(f"    SCHEMA:               {config.POSTGRES_SCHEMA}")
        print(f"    USER:                 {config.POSTGRES_USER}")
        print(f"    SSL MODE:             {config.POSTGRES_SSLMODE}")
    
    if config.SMTP_HOST:
        print(f"\n  SMTP Configuration:")
        print(f"    HOST:                 {config.SMTP_HOST}")
        print(f"    PORT:                 {config.SMTP_PORT}")
        print(f"    USER:                 {config.SMTP_USER}")
        print(f"    USE TLS:              {config.SMTP_USE_TLS}")
    else:
        print(f"\n  SMTP:                   Not configured (OTP codes will print to console)")
        
except Exception as e:
    print(f"  ❌ Error loading config: {e}")
    import traceback
    traceback.print_exc()

# Check 3: Test Storage Backend
print("\n💾 STORAGE BACKEND TEST:")
print("-" * 70)
try:
    from requestbin import db
    print(f"  Backend Type:           {type(db.db).__name__}")
    print(f"  Backend Module:         {type(db.db).__module__}")
    
    # Test bin creation
    print("\n  Testing bin operations...")
    test_bin = db.create_bin(private=False, custom_name="diagnostic_test")
    print(f"    ✅ Create bin:         {test_bin.name}")
    
    # Test bin lookup
    found_bin = db.lookup_bin(test_bin.name)
    print(f"    ✅ Lookup bin:         {found_bin.name}")
    
    # Test bin count
    bin_count = db.count_bins()
    print(f"    ✅ Count bins:         {bin_count}")
    
    print("\n  ✅ Storage backend is working correctly!")
    
except Exception as e:
    print(f"  ❌ Storage backend error: {e}")
    import traceback
    traceback.print_exc()

# Check 4: Test Authentication System
print("\n🔐 AUTHENTICATION SYSTEM TEST:")
print("-" * 70)
try:
    from requestbin import auth_db
    print(f"  Auth Backend Type:      {type(auth_db).__name__}")
    
    # Check admin user
    try:
        admin = auth_db.get_user(config.ADMIN_EMAIL)
        if admin:
            print(f"  ✅ Admin user exists:   {admin.email}")
            print(f"     - Is admin:          {admin.is_admin}")
            print(f"     - Is approved:       {admin.is_approved}")
            print(f"     - Email verified:    {admin.email_verified}")
        else:
            print(f"  ⚠️  Admin user not found")
    except:
        print(f"  ⚠️  Could not check admin user")
    
    # Check user count
    try:
        if hasattr(auth_db, 'users'):
            print(f"  Total users:            {len(auth_db.users)}")
        else:
            print(f"  Total users:            (using PostgreSQL backend)")
    except:
        pass
    
    print("\n  ✅ Authentication system loaded!")
    
except Exception as e:
    print(f"  ❌ Authentication error: {e}")
    import traceback
    traceback.print_exc()

# Check 5: PostgreSQL Connection (if applicable)
if 'postgresql' in config.STORAGE_BACKEND.lower():
    print("\n🐘 POSTGRESQL CONNECTION TEST:")
    print("-" * 70)
    try:
        from requestbin.storage.postgresql import PostgreSQLStorage
        import psycopg2
        
        # Build connection string
        conn_params = {
            'host': config.POSTGRES_HOST,
            'port': config.POSTGRES_PORT,
            'database': config.POSTGRES_DB,
            'user': config.POSTGRES_USER,
        }
        
        if config.POSTGRES_PASSWORD:
            conn_params['password'] = config.POSTGRES_PASSWORD
        
        # Add schema search path
        conn_params['options'] = f'-c search_path={config.POSTGRES_SCHEMA}'
        
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check PostgreSQL version
        cursor.execute('SELECT version()')
        version = cursor.fetchone()[0]
        print(f"  ✅ Connected to PostgreSQL")
        print(f"     Version: {version.split(',')[0]}")
        
        # Check schema exists
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s
        """, (config.POSTGRES_SCHEMA,))
        
        schema_exists = cursor.fetchone()
        if schema_exists:
            print(f"  ✅ Schema '{config.POSTGRES_SCHEMA}' exists")
        else:
            print(f"  ⚠️  Schema '{config.POSTGRES_SCHEMA}' does NOT exist!")
            print(f"     Run: psql -d {config.POSTGRES_DB} -f schema.sql")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
            ORDER BY table_name
        """, (config.POSTGRES_SCHEMA,))
        
        tables = cursor.fetchall()
        if tables:
            print(f"  ✅ Tables in schema '{config.POSTGRES_SCHEMA}':")
            for table in tables:
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {config.POSTGRES_SCHEMA}.{table[0]}
                """)
                count = cursor.fetchone()[0]
                print(f"     - {table[0]:20} ({count} rows)")
        else:
            print(f"  ⚠️  No tables found in schema '{config.POSTGRES_SCHEMA}'!")
            print(f"     Run: psql -d {config.POSTGRES_DB} -f schema.sql")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"  ❌ PostgreSQL connection error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n  💡 Troubleshooting:")
        print(f"     1. Is PostgreSQL running? (pg_ctl status)")
        print(f"     2. Does the database exist? (createdb {config.POSTGRES_DB})")
        print(f"     3. Are credentials correct?")
        print(f"     4. Is the schema initialized? (psql -d {config.POSTGRES_DB} -f schema.sql)")

# Summary
print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
print("\n💡 To run the application:")
print("   With Memory backend:     .\\run-local-memory.ps1")
print("   With PostgreSQL backend: .\\run-local-postgres.ps1")
print("\n")
