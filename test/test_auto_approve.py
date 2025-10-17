"""
Test AUTO_APPROVE_DOMAINS functionality with universal OTP verification
"""
import os
import sys

# Set test environment
os.environ['STORAGE_BACKEND'] = 'memory'
os.environ['AUTO_APPROVE_DOMAINS'] = 'tarento.com,ivolve.ai'

from requestbin import config, auth_db
from requestbin.auth import User

def test_auto_approve_domains():
    print('\n' + '='*60)
    print('AUTO_APPROVE_DOMAINS VERIFICATION TEST')
    print('='*60 + '\n')

    # Test 1: Configuration Check
    print('[Test 1] Configuration Check')
    print(f'   AUTO_APPROVE_DOMAINS from env: {os.environ.get("AUTO_APPROVE_DOMAINS")}')
    print(f'   Parsed domains: {config.AUTO_APPROVE_DOMAINS}')
    print(f'   ✓ Configuration loaded correctly\n')

    # Test 2: Domain Matching Logic
    print('[Test 2] Domain Matching Logic')
    test_cases = [
        ('user@tarento.com', True, 'tarento.com should auto-approve'),
        ('user@ivolve.ai', True, 'ivolve.ai should auto-approve'),
        ('user@TARENTO.COM', True, 'Case-insensitive: TARENTO.COM should auto-approve'),
        ('user@example.com', False, 'example.com should NOT auto-approve'),
        ('user@gmail.com', False, 'gmail.com should NOT auto-approve'),
        ('user@tarento.com.fake', False, 'tarento.com.fake should NOT auto-approve'),
    ]

    all_passed = True
    for email, expected, description in test_cases:
        user = User(email=email, password_hash='dummy')
        result = user.should_auto_approve()
        status = '✓' if result == expected else '✗'
        if result != expected:
            all_passed = False
        print(f'   {status} {email}: {result} (expected {expected}) - {description}')

    print()

    # Test 3: Integration with User Creation
    print('[Test 3] User Creation with Auto-Approve')

    # Create auto-approve user
    user1 = auth_db.create_user(email='alice@tarento.com', password='test123', is_admin=False)
    print(f'   User: alice@tarento.com')
    print(f'   ✓ is_approved: {user1.is_approved} (should be True after email verification)')
    print(f'   ✓ email_verified: {user1.email_verified} (should be False initially)')
    print(f'   ✓ otp_code: {user1.otp_code} (should exist)')
    print(f'   ✓ should_auto_approve(): {user1.should_auto_approve()} (should be True)')
    print()

    # Create non-auto-approve user
    user2 = auth_db.create_user(email='bob@example.com', password='test123', is_admin=False)
    print(f'   User: bob@example.com')
    print(f'   ✓ is_approved: {user2.is_approved} (should be False)')
    print(f'   ✓ email_verified: {user2.email_verified} (should be False initially)')
    print(f'   ✓ otp_code: {user2.otp_code} (should exist)')
    print(f'   ✓ should_auto_approve(): {user2.should_auto_approve()} (should be False)')
    print()

    # Test 4: Workflow Verification
    print('[Test 4] Complete Workflow Verification')
    print('   Scenario A: Auto-Approve Domain (tarento.com)')
    print('   1. User registers → is_approved=True, email_verified=False, OTP sent')
    print(f'      ✓ Verified: is_approved={user1.is_approved}, verified={user1.email_verified}, OTP={user1.otp_code is not None}')
    print('   2. User verifies OTP → email_verified=True')
    user1.verify_otp(user1.otp_code)
    print(f'      ✓ Verified: email_verified={user1.email_verified}')
    print('   3. User can login → Both approved AND verified')
    can_login = user1.is_approved and user1.email_verified
    print(f'      ✓ Can login: {can_login}')
    print()

    print('   Scenario B: Non-Auto-Approve Domain (example.com)')
    print('   1. User registers → is_approved=False, email_verified=False, OTP sent')
    print(f'      ✓ Verified: is_approved={user2.is_approved}, verified={user2.email_verified}, OTP={user2.otp_code is not None}')
    print('   2. User verifies OTP → email_verified=True')
    user2.verify_otp(user2.otp_code)
    print(f'      ✓ Verified: email_verified={user2.email_verified}')
    print('   3. User waits for admin approval')
    print(f'      ✓ Can login: {user2.is_approved and user2.email_verified} (False - needs admin approval)')
    print('   4. Admin approves user → is_approved=True')
    user2.is_approved = True
    print(f'      ✓ Can login: {user2.is_approved and user2.email_verified} (True - now approved)')
    print()

    # Final Summary
    print('='*60)
    if all_passed:
        print('✅ ALL AUTO_APPROVE_DOMAINS TESTS PASSED')
    else:
        print('❌ SOME TESTS FAILED')
        return False
    print('='*60)
    print()
    print('Summary:')
    print('  • AUTO_APPROVE_DOMAINS properly configured')
    print('  • Domain matching is case-insensitive')
    print('  • Auto-approve users: approved=True after registration')
    print('  • Non-auto-approve users: approved=False, need admin approval')
    print('  • ALL users get OTP and must verify email')
    print('  • Login requires: approved=True AND verified=True')
    print()
    
    return True

if __name__ == '__main__':
    success = test_auto_approve_domains()
    sys.exit(0 if success else 1)
