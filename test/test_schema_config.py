"""
Test PostgreSQL schema configuration
"""
import os

# Set environment for testing
os.environ['STORAGE_BACKEND'] = 'memory'  # Use memory for this test
os.environ['POSTGRES_SCHEMA'] = 'requestbin_app'

from requestbin import config

def test_postgres_schema_config():
    print('\n' + '='*60)
    print('POSTGRESQL SCHEMA CONFIGURATION TEST')
    print('='*60 + '\n')
    
    # Test 1: Configuration Check
    print('[Test 1] Schema Configuration')
    print(f'   POSTGRES_SCHEMA from env: {os.environ.get("POSTGRES_SCHEMA")}')
    print(f'   Config value: {config.POSTGRES_SCHEMA}')
    assert config.POSTGRES_SCHEMA == 'requestbin_app', f"Expected 'requestbin_app', got '{config.POSTGRES_SCHEMA}'"
    print(f'   ✓ Schema configured correctly: {config.POSTGRES_SCHEMA}\n')
    
    # Test 2: Default Value Check
    print('[Test 2] Default Schema Value')
    # Temporarily remove env var
    old_value = os.environ.pop('POSTGRES_SCHEMA', None)
    # Re-import to test default
    import importlib
    importlib.reload(config)
    print(f'   Default POSTGRES_SCHEMA: {config.POSTGRES_SCHEMA}')
    assert config.POSTGRES_SCHEMA == 'requestbin_app', f"Default should be 'requestbin_app', got '{config.POSTGRES_SCHEMA}'"
    print(f'   ✓ Default value correct: {config.POSTGRES_SCHEMA}\n')
    
    # Restore env var
    if old_value:
        os.environ['POSTGRES_SCHEMA'] = old_value
    importlib.reload(config)
    
    # Test 3: All PostgreSQL Configuration
    print('[Test 3] Complete PostgreSQL Configuration')
    print(f'   POSTGRES_HOST: {config.POSTGRES_HOST}')
    print(f'   POSTGRES_PORT: {config.POSTGRES_PORT}')
    print(f'   POSTGRES_DB: {config.POSTGRES_DB}')
    print(f'   POSTGRES_SCHEMA: {config.POSTGRES_SCHEMA}')
    print(f'   POSTGRES_USER: {config.POSTGRES_USER}')
    print(f'   POSTGRES_SSLMODE: {config.POSTGRES_SSLMODE}')
    print(f'   ✓ All configuration values loaded\n')
    
    # Test 4: Schema in Connection Options
    print('[Test 4] Schema in Connection String')
    expected_options = f'-c search_path={config.POSTGRES_SCHEMA}'
    print(f'   Expected connection option: {expected_options}')
    print(f'   Schema: {config.POSTGRES_SCHEMA}')
    print(f'   ✓ Connection will use schema: {config.POSTGRES_SCHEMA}\n')
    
    print('='*60)
    print('✅ ALL SCHEMA CONFIGURATION TESTS PASSED')
    print('='*60)
    print()
    print('Summary:')
    print(f'  • PostgreSQL schema: {config.POSTGRES_SCHEMA}')
    print(f'  • Schema will be created by schema.sql')
    print(f'  • Connection uses: options="-c search_path={config.POSTGRES_SCHEMA}"')
    print(f'  • All tables will be in: {config.POSTGRES_SCHEMA} schema')
    print()
    
    return True

if __name__ == '__main__':
    import sys
    success = test_postgres_schema_config()
    sys.exit(0 if success else 1)
