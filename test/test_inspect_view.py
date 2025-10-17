#!/usr/bin/env python
"""
Test script for the new split-panel inspect view.
Sends various types of requests to demonstrate the new UI features.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
import time
import json

BASE_URL = "http://localhost:3200"
BIN_NAME = "6b4crirj"  # Use existing bin or create new one

def send_test_requests():
    """Send various types of requests to test the inspect view."""
    
    bin_url = f"{BASE_URL}/{BIN_NAME}"
    
    print("=" * 70)
    print("Testing RequestBin Enterprise Split-Panel Inspect View")
    print("=" * 70)
    print(f"\nSending test requests to: {bin_url}")
    print(f"View results at: {bin_url}?inspect\n")
    
    tests = [
        {
            "name": "JSON POST Request",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": json.dumps({
                "user": "test_user",
                "action": "login",
                "timestamp": datetime.now().isoformat(),
                "metadata": {"browser": "Chrome", "platform": "Windows"}
            })
        },
        {
            "name": "Form URL-Encoded POST",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": "username=testuser&password=secret123&remember=true"
        },
        {
            "name": "GET Request with Query Params",
            "method": "GET",
            "params": {
                "search": "test query",
                "page": "1",
                "limit": "10",
                "sort": "date"
            }
        },
        {
            "name": "XML POST Request",
            "method": "POST",
            "headers": {"Content-Type": "application/xml"},
            "data": '<?xml version="1.0"?><request><user>testuser</user><action>update</action></request>'
        },
        {
            "name": "Plain Text POST",
            "method": "POST",
            "headers": {"Content-Type": "text/plain"},
            "data": "This is a plain text message for testing.\nIt has multiple lines.\nAnd special chars: @#$%"
        },
        {
            "name": "PUT Request with JSON",
            "method": "PUT",
            "headers": {"Content-Type": "application/json"},
            "data": json.dumps({"id": 123, "status": "updated", "updated_at": datetime.now().isoformat()})
        },
        {
            "name": "DELETE Request",
            "method": "DELETE",
            "params": {"id": "456", "confirm": "true"}
        },
        {
            "name": "PATCH Request",
            "method": "PATCH",
            "headers": {"Content-Type": "application/json"},
            "data": json.dumps({"field": "email", "value": "newemail@example.com"})
        },
        {
            "name": "Form Data POST",
            "method": "POST",
            "data": {
                "title": "Test Form",
                "description": "Testing form-data content type",
                "priority": "high",
                "tags": "test,demo,inspect"
            }
        },
        {
            "name": "GET with Custom Headers",
            "method": "GET",
            "headers": {
                "X-Custom-Header": "CustomValue",
                "X-API-Key": "secret-api-key-123",
                "X-Request-ID": "req-12345-67890",
                "User-Agent": "TestAgent/1.0"
            }
        }
    ]
    
    success_count = 0
    
    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}] {test['name']}")
        print("-" * 50)
        
        try:
            # Prepare request
            method = test.get("method", "GET")
            headers = test.get("headers", {})
            data = test.get("data")
            params = test.get("params")
            
            # Send request
            response = requests.request(
                method=method,
                url=bin_url,
                headers=headers,
                data=data,
                params=params,
                timeout=5
            )
            
            # Display result
            print(f"   Status: {response.status_code} {response.reason}")
            print(f"   Method: {method}")
            if headers:
                print(f"   Content-Type: {headers.get('Content-Type', 'N/A')}")
            if data:
                data_size = len(data) if isinstance(data, str) else len(str(data))
                print(f"   Data Size: {data_size} bytes")
            if params:
                print(f"   Query Params: {len(params)} parameters")
            
            print(f"   ✓ Request sent successfully")
            success_count += 1
            
            # Small delay between requests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"Test Summary: {success_count}/{len(tests)} requests sent successfully")
    print("=" * 70)
    print(f"\n📊 View the new split-panel inspect view at:")
    print(f"   {bin_url}?inspect")
    print("\n✨ Features to test:")
    print("   • Click any request in the left panel to view details")
    print("   • Check color-coded HTTP method badges")
    print("   • Verify content-type classifications (json, form-data, xml, etc.)")
    print("   • Test the copy-to-clipboard functionality")
    print("   • Notice the date/time format: YYYY-MM-DD HH:mm:ss")
    print("   • See request sizes and source IPs")
    print()

if __name__ == "__main__":
    try:
        send_test_requests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
