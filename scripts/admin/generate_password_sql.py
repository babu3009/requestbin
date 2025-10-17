#!/usr/bin/env python
"""
Generate Password Hash and SQL for Admin Password Change
"""

import sys
from werkzeug.security import generate_password_hash

def generate_password_change_sql():
    """Generate SQL to change admin password"""
    
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
        return
    
    # Confirm password
    confirm_password = input("Confirm new password: ").strip()
    if new_password != confirm_password:
        print("\n❌ Error: Passwords do not match!")
        return
    
    # Generate hash
    print("\n🔐 Generating password hash...")
    password_hash = generate_password_hash(new_password)
    
    # Generate SQL
    sql = f"""-- Change Admin Password for {admin_email}
SET search_path TO requestbin_app;

UPDATE users 
SET password_hash = '{password_hash}',
    updated_at = NOW()
WHERE email = '{admin_email}';

-- Verify the update
SELECT email, is_admin, is_approved, updated_at 
FROM users 
WHERE email = '{admin_email}';
"""
    
    print("\n" + "=" * 70)
    print("✅ Password hash generated successfully!")
    print("=" * 70)
    
    print("\n📋 SQL Command to run:")
    print("\n" + "-" * 70)
    print(sql)
    print("-" * 70)
    
    # Save to file
    output_file = "update_admin_password.sql"
    with open(output_file, 'w') as f:
        f.write(sql)
    
    print(f"\n💾 SQL saved to: {output_file}")
    print("\n🚀 To apply this change, run one of the following:")
    print("\n   Option 1 - Using psql:")
    print(f"   psql -h localhost -p 55234 -U f21e30667747 -d gmImNcMNjRlT -f {output_file}")
    print("\n   Option 2 - Using Python script:")
    print("   python apply_password_change.py")
    print("\n   Option 3 - Manual:")
    print("   Copy the SQL above and run it in your PostgreSQL client")
    print("\n" + "=" * 70)
    print()

if __name__ == '__main__':
    try:
        generate_password_change_sql()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)
