#!/usr/bin/env python3
"""
Test script for cron endpoints.
This script can be used to test the cron endpoints locally before deployment.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
CRON_SECRET = "your-cron-secret-here"  # Should match what's in your env

# Test endpoints
CRON_ENDPOINTS = [
    "/api/cron/reminder-dispatcher",
    "/api/cron/overdue-scanner",
]

def test_cron_endpoint(endpoint):
    """Test a single cron endpoint with proper headers."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "X-Cron-Secret": CRON_SECRET,
        "Content-Type": "application/json"
    }

    print(f"\nTesting: {endpoint}")
    print(f"URL: {url}")

    try:
        response = requests.post(url, headers=headers)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response Body: {json.dumps(data, indent=2)}")
                return True, data
            except json.JSONDecodeError:
                print(f"Response Text: {response.text}")
                return False, response.text
        else:
            print(f"Error Response: {response.text}")
            return False, response.text

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Make sure the server is running.")
        print(f"Run: cd server && uvicorn main:app --reload")
        return False, "Connection error"
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False, str(e)

def test_cron_security():
    """Test that cron endpoints reject requests without proper headers."""
    print("\n" + "="*60)
    print("Testing Security (should reject unauthorized requests)")
    print("="*60)

    for endpoint in CRON_ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"

        # Test without any headers
        print(f"\nTesting {endpoint} without headers:")
        response = requests.post(url)
        print(f"Status Code (should be 403): {response.status_code}")

        # Test with wrong secret
        headers = {"X-Cron-Secret": "wrong-secret"}
        print(f"\nTesting {endpoint} with wrong secret:")
        response = requests.post(url, headers=headers)
        print(f"Status Code (should be 403): {response.status_code}")

def test_health_check():
    """Test the health check endpoint."""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)

    url = f"{BASE_URL}/api/health"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def main():
    """Main test function."""
    print("="*60)
    print("CRON ENDPOINT TESTER")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*60)

    # Test health check first
    if not test_health_check():
        print("\nHealth check failed. Make sure server is running.")
        print("Run: cd server && uvicorn main:app --reload")
        return

    # Test security first
    test_cron_security()

    # Test valid cron endpoints
    print("\n" + "="*60)
    print("Testing Valid Cron Endpoints")
    print("="*60)

    results = []
    for endpoint in CRON_ENDPOINTS:
        success, result = test_cron_endpoint(endpoint)
        results.append((endpoint, success))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for endpoint, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {endpoint}")

    # Final instructions
    print("\n" + "="*60)
    print("NEXT STEPS FOR DEPLOYMENT")
    print("="*60)
    print("1. Update the CRON_SECRET in test_cron.py to match your actual secret")
    print("2. Set environment variable CRON_SECRET in production")
    print("3. Deploy to Vercel with vercel.json configuration")
    print("4. Configure cron schedules in Vercel dashboard if needed")

if __name__ == "__main__":
    main()