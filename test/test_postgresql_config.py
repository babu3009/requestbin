#!/usr/bin/env python
"""
Test script to verify PostgreSQL storage configuration
Run this to test your PostgreSQL setup before deployment
"""

import os
import json
import sys

def test_postgresql_local():
    """Test local PostgreSQL configuration"""
    print("Testing Local PostgreSQL Configuration...")
    print("=" * 50)
    
    # Set test environment
    os.environ['REALM'] = 'prod'
    os.environ['STORAGE_BACKEND'] = 'postgresql'
    
    # Use default local settings or environment variables
    postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
    postgres_port = os.environ.get('POSTGRES_PORT', '5432')
    postgres_db = os.environ.get('POSTGRES_DB', 'requestbin')
    postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
    
    print(f"PostgreSQL Host: {postgres_host}")
    print(f"PostgreSQL Port: {postgres_port}")
    print(f"PostgreSQL Database: {postgres_db}")
    print(f"PostgreSQL User: {postgres_user}")
    print()
    
    try:
        # Import configuration
        import requestbin.config as config
        
        print("✓ Configuration loaded successfully")
        print(f"✓ Storage Backend: {config.STORAGE_BACKEND}")
        print(f"✓ PostgreSQL Host: {config.POSTGRES_HOST}")
        print(f"✓ PostgreSQL Port: {config.POSTGRES_PORT}")
        print(f"✓ PostgreSQL Database: {config.POSTGRES_DB}")
        print(f"✓ PostgreSQL SSL Mode: {config.POSTGRES_SSLMODE}")
        print()
        
        # Test PostgreSQL storage initialization
        from requestbin.storage.postgresql import PostgreSQLStorage
        
        print("Initializing PostgreSQL storage...")
        storage = PostgreSQLStorage(bin_ttl=3600)
        print("✓ PostgreSQL storage initialized successfully")
        print()
        
        # Test connection by counting bins
        try:
            bin_count = storage.count_bins()
            request_count = storage.count_requests()
            
            print("✓ PostgreSQL connection successful!")
            print(f"  Current bins: {bin_count}")
            print(f"  Total requests: {request_count}")
            print()
            
            # Test creating a bin
            print("Testing bin creation...")
            test_bin = storage.create_bin(private=False, custom_name="test_bin_" + str(int(os.times()[4])))
            print(f"✓ Created test bin: {test_bin.name}")
            
            # Test looking up the bin
            print("Testing bin lookup...")
            retrieved_bin = storage.lookup_bin(test_bin.name)
            print(f"✓ Retrieved bin: {retrieved_bin.name}")
            print()
            
            return True
        except Exception as e:
            print(f"✗ PostgreSQL connection failed: {e}")
            print("  Make sure PostgreSQL is running and credentials are correct")
            print("  Run: psql -U {user} -d {database} -f schema.sql")
            return False
            
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sap_btp_config():
    """Test SAP BTP PostgreSQL service configuration"""
    print("\nTesting SAP BTP PostgreSQL Configuration...")
    print("=" * 50)
    
    # Simulate SAP BTP VCAP_SERVICES environment
    vcap_services = {
        "postgresql": [{
            "credentials": {
                "hostname": "postgresql.example.com",
                "port": 5432,
                "dbname": "requestbin_db",
                "username": "requestbin_user",
                "password": "test_password",
                "sslmode": "require"
            },
            "name": "requestbin-postgresql"
        }]
    }
    
    # Set environment variables to simulate SAP BTP
    os.environ['VCAP_SERVICES'] = json.dumps(vcap_services)
    os.environ['REALM'] = 'prod'
    os.environ['STORAGE_BACKEND'] = 'postgresql'
    
    try:
        # Reload configuration module to pick up new environment
        import importlib
        import requestbin.config as config
        importlib.reload(config)
        
        print("✓ Configuration loaded successfully")
        print(f"✓ Storage Backend: {config.STORAGE_BACKEND}")
        print(f"✓ PostgreSQL Host: {config.POSTGRES_HOST}")
        print(f"✓ PostgreSQL Port: {config.POSTGRES_PORT}")
        print(f"✓ PostgreSQL Database: {config.POSTGRES_DB}")
        print(f"✓ PostgreSQL User: {config.POSTGRES_USER}")
        print(f"✓ PostgreSQL SSL Mode: {config.POSTGRES_SSLMODE}")
        
        # Verify VCAP_SERVICES was parsed correctly
        if config.POSTGRES_HOST == "postgresql.example.com":
            print("✓ VCAP_SERVICES parsed correctly")
            print()
            print("⚠️  Note: Cannot test actual connection (simulated environment)")
            return True
        else:
            print("✗ VCAP_SERVICES not parsed correctly")
            return False
            
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("PostgreSQL Storage Configuration Test")
    print("=" * 50)
    print()
    
    # Test local configuration
    local_success = test_postgresql_local()
    
    # Test SAP BTP configuration
    sap_success = test_sap_btp_config()
    
    print()
    print("=" * 50)
    print("Test Summary:")
    print(f"  Local PostgreSQL: {'✓ PASSED' if local_success else '✗ FAILED'}")
    print(f"  SAP BTP Config: {'✓ PASSED' if sap_success else '✗ FAILED'}")
    print()
    
    if local_success:
        print("🎉 PostgreSQL storage is configured correctly!")
        print()
        print("Next steps:")
        print("1. Ensure schema.sql has been run on your database")
        print("2. Set STORAGE_BACKEND=postgresql in your environment")
        print("3. Deploy to SAP BTP using: cf push -f manifest-postgresql.yml")
    else:
        print("⚠️  Please fix the configuration issues above.")
        print()
        print("Common fixes:")
        print("1. Install PostgreSQL: brew install postgresql (macOS) or apt-get install postgresql (Linux)")
        print("2. Create database: createdb requestbin")
        print("3. Run schema: psql -d requestbin -f schema.sql")
        print("4. Set environment variables: export POSTGRES_HOST=localhost POSTGRES_DB=requestbin")
    
    return 0 if (local_success and sap_success) else 1

if __name__ == "__main__":
    sys.exit(main())
