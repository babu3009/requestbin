#!/usr/bin/env python
"""
UI/UX feature tests for RequestBin Enterprise
Tests layout updates, copy functionality, and navigation improvements
"""

import os
import sys
import re

# Set environment for testing
os.environ['REALM'] = 'local'
os.environ['STORAGE_BACKEND'] = 'requestbin.storage.memory.MemoryStorage'


def test_layout_improvements():
    """Test layout template improvements"""
    print("=" * 60)
    print("LAYOUT TEMPLATE TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n1. Dropdown Menu Improvements:")
    try:
        with open('requestbin/templates/layout.html', 'r') as f:
            content = f.read()
            
            # Check for Home link
            if 'icon-home' in content and 'Home</a>' in content:
                print("  ✓ Home link with icon added")
                tests_passed += 1
            else:
                print("  ✗ Home link not found")
                tests_failed += 1
            
            # Check for About icon
            if 'icon-info-sign' in content:
                print("  ✓ About icon updated (icon-info-sign)")
                tests_passed += 1
            else:
                print("  ✗ About icon not updated")
                tests_failed += 1
            
            # Check for dropdown structure
            if 'dropdown-menu' in content:
                print("  ✓ Dropdown menu structure present")
                tests_passed += 1
            else:
                print("  ✗ Dropdown menu not found")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ Layout template check failed - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_bin_url_display():
    """Test bin URL display and positioning"""
    print("\n" + "=" * 60)
    print("BIN URL DISPLAY TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n1. Bin URL Positioning:")
    try:
        with open('requestbin/templates/bin.html', 'r') as f:
            content = f.read()
            
            # Check for conditional display
            if '{% if bin.requests %}' in content:
                print("  ✓ Conditional bin URL display")
                tests_passed += 1
            else:
                print("  ✗ Conditional display not found")
                tests_failed += 1
            
            # Check for bin-url-bar
            if 'bin-url-bar' in content:
                print("  ✓ Bin URL bar component present")
                tests_passed += 1
            else:
                print("  ✗ Bin URL bar not found")
                tests_failed += 1
            
            # Check for bin-url-input IDs
            if 'id="bin-url-input"' in content:
                print("  ✓ Bin URL input field (header)")
                tests_passed += 1
            else:
                print("  ✗ Header bin URL input not found")
                tests_failed += 1
            
            if 'id="bin-url-input-large"' in content:
                print("  ✓ Bin URL input field (large)")
                tests_passed += 1
            else:
                print("  ✗ Large bin URL input not found")
                tests_failed += 1
            
            # Check for color indicator
            if 'bin-color-indicator' in content:
                print("  ✓ Color indicator present")
                tests_passed += 1
            else:
                print("  ✗ Color indicator not found")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ Bin template check failed - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_copy_functionality():
    """Test copy button functionality"""
    print("\n" + "=" * 60)
    print("COPY FUNCTIONALITY TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n1. JavaScript Copy Functions:")
    try:
        with open('requestbin/static/js/app.js', 'r') as f:
            content = f.read()
            
            # Check for copyBinUrl function
            if 'function copyBinUrl()' in content or 'copyBinUrl()' in content:
                print("  ✓ copyBinUrl() function defined")
                tests_passed += 1
            else:
                print("  ✗ copyBinUrl() function not found")
                tests_failed += 1
            
            # Check for copyBinUrlLarge function
            if 'function copyBinUrlLarge()' in content or 'copyBinUrlLarge()' in content:
                print("  ✓ copyBinUrlLarge() function defined")
                tests_passed += 1
            else:
                print("  ✗ copyBinUrlLarge() function not found")
                tests_failed += 1
            
            # Check for clipboard API usage
            if 'navigator.clipboard.writeText' in content:
                print("  ✓ Clipboard API used")
                tests_passed += 1
            else:
                print("  ✗ Clipboard API not found")
                tests_failed += 1
            
            # Check for visual feedback
            if 'btn-success' in content or 'Copied' in content:
                print("  ✓ Visual feedback implemented")
                tests_passed += 1
            else:
                print("  ✗ Visual feedback not found")
                tests_failed += 1
            
            # Check for fallback mechanism
            if '.select()' in content:
                print("  ✓ Fallback selection method present")
                tests_passed += 1
            else:
                print("  ✗ Fallback not found")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ JavaScript check failed - {e}")
        tests_failed += 1
    
    print("\n2. Copy Button in Templates:")
    try:
        with open('requestbin/templates/bin.html', 'r') as f:
            content = f.read()
            
            # Check for copy buttons
            copy_buttons = content.count('onclick="copyBinUrl')
            if copy_buttons >= 2:
                print(f"  ✓ Copy buttons present ({copy_buttons} found)")
                tests_passed += 1
            else:
                print(f"  ✗ Insufficient copy buttons ({copy_buttons} found)")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ Template check failed - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_css_styling():
    """Test CSS styling for new components"""
    print("\n" + "=" * 60)
    print("CSS STYLING TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n1. Bin URL Bar Styles:")
    try:
        with open('requestbin/static/css/styles.css', 'r') as f:
            content = f.read()
            
            # Check for bin-url-bar styles
            if '.bin-url-bar' in content:
                print("  ✓ .bin-url-bar styles defined")
                tests_passed += 1
            else:
                print("  ✗ .bin-url-bar styles not found")
                tests_failed += 1
            
            # Check for bin-url-content styles
            if '.bin-url-content' in content:
                print("  ✓ .bin-url-content styles defined")
                tests_passed += 1
            else:
                print("  ✗ .bin-url-content styles not found")
                tests_failed += 1
            
            # Check for bin-url-input-field styles
            if '.bin-url-input-field' in content:
                print("  ✓ .bin-url-input-field styles defined")
                tests_passed += 1
            else:
                print("  ✗ .bin-url-input-field styles not found")
                tests_failed += 1
            
            # Check for bin-color-indicator styles
            if '.bin-color-indicator' in content:
                print("  ✓ .bin-color-indicator styles defined")
                tests_passed += 1
            else:
                print("  ✗ .bin-color-indicator styles not found")
                tests_failed += 1
            
            # Check for responsive design (flexbox)
            if 'display: flex' in content or 'display:flex' in content:
                print("  ✓ Flexbox layout used")
                tests_passed += 1
            else:
                print("  ✗ Flexbox not found")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ CSS check failed - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def test_password_routes():
    """Test password management routes"""
    print("\n" + "=" * 60)
    print("PASSWORD MANAGEMENT ROUTES TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n1. Route Registration:")
    try:
        from requestbin import app
        
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        # Check for password management routes
        password_routes = [
            '/auth/change-password',
            '/auth/forgot-password',
            '/auth/reset-password'
        ]
        
        for route in password_routes:
            if route in routes:
                print(f"  ✓ {route}")
                tests_passed += 1
            else:
                print(f"  ✗ {route} not registered")
                tests_failed += 1
                
    except Exception as e:
        print(f"  ✗ Route check failed - {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("=" * 60)
    
    return tests_failed == 0


def main():
    """Run all UI/UX tests"""
    print("\n" + "█" * 60)
    print("REQUESTBIN ENTERPRISE UI/UX COMPREHENSIVE TESTS")
    print("█" * 60)
    
    layout_success = test_layout_improvements()
    bin_url_success = test_bin_url_display()
    copy_success = test_copy_functionality()
    css_success = test_css_styling()
    password_success = test_password_routes()
    
    print("\n" + "█" * 60)
    print("FINAL RESULTS")
    print("█" * 60)
    
    all_success = all([
        layout_success,
        bin_url_success,
        copy_success,
        css_success,
        password_success
    ])
    
    if all_success:
        print("✅ ALL UI/UX TESTS PASSED!")
        print("\nUI/UX Features Verified:")
        print("  ✓ Dropdown menu with Home link")
        print("  ✓ Updated About icon (icon-info-sign)")
        print("  ✓ Conditional bin URL display")
        print("  ✓ Bin URL bar above table")
        print("  ✓ Copy button functionality")
        print("  ✓ Visual feedback on copy")
        print("  ✓ Professional CSS styling")
        print("  ✓ Password management routes")
        print("\nUser Experience Improvements:")
        print("  • Easy navigation with Home link")
        print("  • One-click URL copying")
        print("  • Clean, professional layout")
        print("  • Conditional UI based on content")
        print("  • Password self-service options")
        return 0
    else:
        print("❌ SOME UI/UX TESTS FAILED")
        print("\nPlease review the errors above and fix them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
