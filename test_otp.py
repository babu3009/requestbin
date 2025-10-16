"""
Test OTP Email Verification Functionality
Tests OTP generation, validation, expiry, and email workflow
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Set test configuration before importing requestbin
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'memory'

def test_otp_functionality():
    """Test OTP generation, verification, and expiry"""
    print("\n" + "="*60)
    print("TESTING OTP EMAIL VERIFICATION FUNCTIONALITY")
    print("="*60)
    
    from requestbin.auth import User
    from requestbin import config
    
    test_results = []
    
    # Test 1: OTP Generation
    print("\n[Test 1] OTP Generation")
    user = User(email='test@tarento.com')
    otp = user.generate_otp()
    
    assert user.otp_code is not None, "OTP code should be generated"
    assert len(user.otp_code) == 6, "OTP should be 6 digits"
    assert user.otp_code.isdigit(), "OTP should contain only digits"
    assert user.otp_created_at is not None, "OTP creation time should be set"
    print(f"   ✓ Generated OTP: {user.otp_code}")
    print(f"   ✓ OTP length: {len(user.otp_code)} digits")
    print(f"   ✓ OTP created at: {user.otp_created_at}")
    test_results.append(("OTP Generation", "PASSED"))
    
    # Test 2: OTP Validity Check (fresh OTP)
    print("\n[Test 2] OTP Validity Check (Fresh OTP)")
    is_valid = user.is_otp_valid()
    assert is_valid == True, "Fresh OTP should be valid"
    print(f"   ✓ Fresh OTP is valid: {is_valid}")
    test_results.append(("OTP Validity (Fresh)", "PASSED"))
    
    # Test 3: OTP Verification (Correct Code)
    print("\n[Test 3] OTP Verification (Correct Code)")
    correct_otp = user.otp_code
    result = user.verify_otp(correct_otp)
    assert result == True, "Correct OTP should verify successfully"
    assert user.email_verified == True, "Email should be marked as verified"
    assert user.otp_code is None, "OTP should be cleared after verification"
    print(f"   ✓ OTP verified successfully")
    print(f"   ✓ Email verified status: {user.email_verified}")
    print(f"   ✓ OTP cleared after verification: {user.otp_code is None}")
    test_results.append(("OTP Verification (Correct)", "PASSED"))
    
    # Test 4: OTP Verification (Incorrect Code)
    print("\n[Test 4] OTP Verification (Incorrect Code)")
    user2 = User(email='test2@tarento.com')
    user2.generate_otp()
    wrong_otp = '999999'
    result = user2.verify_otp(wrong_otp)
    assert result == False, "Wrong OTP should fail verification"
    assert user2.email_verified == False, "Email should not be verified"
    print(f"   ✓ Wrong OTP rejected: {result == False}")
    print(f"   ✓ Email verified status: {user2.email_verified}")
    test_results.append(("OTP Verification (Incorrect)", "PASSED"))
    
    # Test 5: OTP Expiry Check
    print("\n[Test 5] OTP Expiry (Simulated)")
    user3 = User(email='test3@tarento.com')
    user3.generate_otp()
    
    # Simulate expired OTP (set to 25 hours ago)
    user3.otp_created_at = time.time() - (25 * 3600)  # 25 hours ago
    
    is_valid = user3.is_otp_valid()
    assert is_valid == False, "Expired OTP should be invalid"
    
    result = user3.verify_otp(user3.otp_code)
    assert result == False, "Expired OTP should fail verification"
    print(f"   ✓ Expired OTP is invalid: {is_valid == False}")
    print(f"   ✓ Expired OTP verification failed: {result == False}")
    test_results.append(("OTP Expiry", "PASSED"))
    
    # Test 6: OTP Expiry Time Calculation
    print("\n[Test 6] OTP Expiry Time Calculation")
    user4 = User(email='test4@tarento.com')
    user4.generate_otp()
    
    expiry_time = user4.get_otp_expiry_time()
    assert expiry_time > 0, "Expiry time should be positive for valid OTP"
    assert expiry_time <= 86400, "Expiry time should not exceed 24 hours"
    
    hours = int(expiry_time // 3600)
    minutes = int((expiry_time % 3600) // 60)
    print(f"   ✓ Expiry time: {hours}h {minutes}m")
    print(f"   ✓ Expiry time in seconds: {expiry_time}")
    test_results.append(("OTP Expiry Calculation", "PASSED"))
    
    # Test 7: Auto-Approve Domain Logic
    print("\n[Test 7] Auto-Approve Domain Logic")
    user_tarento = User(email='user@tarento.com')
    user_ivolve = User(email='user@ivolve.ai')
    user_other = User(email='user@example.com')
    
    assert user_tarento.should_auto_approve() == True, "tarento.com should auto-approve"
    assert user_ivolve.should_auto_approve() == True, "ivolve.ai should auto-approve"
    assert user_other.should_auto_approve() == False, "example.com should not auto-approve"
    
    print(f"   ✓ tarento.com auto-approve: {user_tarento.should_auto_approve()}")
    print(f"   ✓ ivolve.ai auto-approve: {user_ivolve.should_auto_approve()}")
    print(f"   ✓ example.com auto-approve: {user_other.should_auto_approve()}")
    test_results.append(("Auto-Approve Domain", "PASSED"))
    
    # Test 8: Memory Storage with OTP
    print("\n[Test 8] Memory Storage with OTP Fields")
    from requestbin.auth_storage import MemoryAuthStorage
    
    storage = MemoryAuthStorage()
    
    # Create user with auto-approve domain
    user = storage.create_user('newuser@tarento.com', 'password123')
    assert user.is_approved == True, "Auto-approve domain should be approved"
    assert user.email_verified == False, "Email should not be verified yet"
    assert user.otp_code is not None, "OTP should be generated"
    
    print(f"   ✓ User created: {user.email}")
    print(f"   ✓ Is approved: {user.is_approved}")
    print(f"   ✓ Email verified: {user.email_verified}")
    print(f"   ✓ OTP generated: {user.otp_code}")
    
    # Verify OTP
    otp_code = user.otp_code
    user.verify_otp(otp_code)
    storage.update_user(user)
    
    # Retrieve and check
    retrieved = storage.get_user('newuser@tarento.com')
    assert retrieved.email_verified == True, "Email should be verified after update"
    print(f"   ✓ Email verified after OTP: {retrieved.email_verified}")
    test_results.append(("Memory Storage OTP", "PASSED"))
    
    # Test 9: Non-Auto-Approve User (Now Gets OTP Too!)
    print("\n[Test 9] Non-Auto-Approve User (Also Gets OTP)")
    user_regular = storage.create_user('regular@example.com', 'password123')
    assert user_regular.is_approved == False, "Regular user should not be approved"
    assert user_regular.email_verified == False, "Regular user email not verified"
    assert user_regular.otp_code is not None, "Regular user SHOULD have OTP now"
    
    print(f"   ✓ Regular user approved: {user_regular.is_approved}")
    print(f"   ✓ Email verified: {user_regular.email_verified}")
    print(f"   ✓ OTP code: {user_regular.otp_code}")
    print(f"   ✓ All users get OTP for email verification")
    test_results.append(("Non-Auto-Approve User", "PASSED"))
    
    # Test 10: Admin User (No OTP Required)
    print("\n[Test 10] Admin User (No OTP Required)")
    admin = storage.get_user(config.ADMIN_EMAIL)
    assert admin.is_admin == True, "Admin should have admin flag"
    assert admin.is_approved == True, "Admin should be approved"
    assert admin.email_verified == True, "Admin email should be verified"
    
    print(f"   ✓ Admin user: {admin.email}")
    print(f"   ✓ Is admin: {admin.is_admin}")
    print(f"   ✓ Is approved: {admin.is_approved}")
    print(f"   ✓ Email verified: {admin.email_verified}")
    test_results.append(("Admin User", "PASSED"))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, status in test_results if status == "PASSED")
    total = len(test_results)
    
    for test_name, status in test_results:
        status_icon = "✓" if status == "PASSED" else "✗"
        print(f"   {status_icon} {test_name}: {status}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("🎉 ALL OTP TESTS PASSED! 🎉\n")
        return 0
    else:
        print("❌ SOME TESTS FAILED\n")
        return 1


if __name__ == '__main__':
    exit_code = test_otp_functionality()
    sys.exit(exit_code)
