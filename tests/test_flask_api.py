#!/usr/bin/env python3
"""
Test script for Flask API endpoints.
Run this after starting the Flask app to test all endpoints.
"""

import requests
import json
import time
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint."""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_generate_single_facture():
    """Test single facture generation endpoint."""
    print("\nTesting single facture generation...")
    
    # Sample facture data
    facture_data = {
        "facture_id": "TEST-001",
        "client": {
            "first_name": "Test Client",
            "last_name": "Example",
            "location": "Montreal, QC"
        },
        "items": [
            {
                "prix_unitaire": 25.0,
                "quantite": 2,
                "frais": 5.0
            },
            {
                "prix_unitaire": 15.0,
                "quantite": 1,
                "frais": 0.0
            }
        ],
        "date_emission": datetime.now().isoformat(),
        "date_service": (datetime.now() + timedelta(days=30)).isoformat(),
        "status": "A_PAYER"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/factures/generate",
            json=facture_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            # Check if PDF content is returned
            if response.headers.get('content-type') == 'application/pdf':
                print(f"✓ Single facture generated successfully")
                print(f"  PDF size: {len(response.content)} bytes")
                return True
            else:
                print(f"✗ Unexpected content type: {response.headers.get('content-type')}")
                return False
        else:
            print(f"✗ Single facture generation failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Single facture generation error: {e}")
        return False

def test_get_factures_status():
    """Test getting factures status endpoint."""
    print("\nTesting get factures status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/factures/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Factures status retrieved successfully")
            print(f"  Total factures: {data.get('total_count', 0)}")
            print(f"  Sample factures: {data.get('factures', [])[:2]}")
            return True
        else:
            print(f"✗ Get factures status failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Get factures status error: {e}")
        return False

def test_get_statistics():
    """Test getting statistics endpoint."""
    print("\nTesting get statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/statistics")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Statistics retrieved successfully")
            print(f"  Total factures: {data.get('total_factures', 0)}")
            print(f"  Status distribution: {data.get('status_distribution', {})}")
            print(f"  Total amount: {data.get('total_amount', 0)}$")
            print(f"  Total amount TTC: {data.get('total_amount_ttc', 0)}$")
            return True
        else:
            print(f"✗ Get statistics failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Get statistics error: {e}")
        return False

def test_batch_generation():
    """Test batch facture generation endpoint."""
    print("\nTesting batch facture generation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/factures/generate-batch",
            json={"filter_status": "A_PAYER"},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Batch generation completed successfully")
            print(f"  Statistics: {data.get('statistics', {})}")
            return True
        else:
            print(f"✗ Batch generation failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Batch generation error: {e}")
        return False

def test_error_handling():
    """Test error handling endpoints."""
    print("\nTesting error handling...")
    
    # Test 404
    try:
        response = requests.get(f"{BASE_URL}/api/nonexistent")
        if response.status_code == 404:
            print("✓ 404 error handling works")
        else:
            print(f"✗ 404 error handling failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 404 test error: {e}")
        return False
    
    # Test invalid JSON
    try:
        response = requests.post(
            f"{BASE_URL}/api/factures/generate",
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code in [400, 500]:
            print("✓ Invalid JSON error handling works")
        else:
            print(f"✗ Invalid JSON error handling failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Invalid JSON test error: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Flask API Testing Suite")
    print("=" * 50)
    
    # Wait a bit for Flask to start
    print("Waiting for Flask app to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_check),
        ("Single Facture Generation", test_generate_single_facture),
        ("Get Factures Status", test_get_factures_status),
        ("Get Statistics", test_get_statistics),
        ("Batch Generation", test_batch_generation),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Flask API is working correctly.")
    else:
        print("❌ Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
