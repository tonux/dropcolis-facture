#!/usr/bin/env python3
"""
Quick test to verify all Flask API components work together.
This test doesn't start the server, just checks the configuration and imports.
"""

import sys
import os

def run_quick_test():
    """Run a quick test of all components."""
    print("🚀 Quick Test - Flask API Components")
    print("=" * 40)
    
    tests = []
    
    # Test 1: Configuration
    try:
        from api_config import config
        config.print_config()
        print("✓ API configuration loaded")
        tests.append(("Configuration", True))
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        tests.append(("Configuration", False))
    
    # Test 2: Flask app import
    try:
        from app import app, generator
        print("✓ Flask app imported")
        print(f"  Routes: {len(list(app.url_map.iter_rules()))}")
        tests.append(("Flask App", True))
    except Exception as e:
        print(f"✗ Flask app import failed: {e}")
        tests.append(("Flask App", False))
    
    # Test 3: Generator functionality
    try:
        if generator:
            config_keys = list(generator.config.keys())
            print(f"✓ Generator initialized with config: {config_keys}")
            tests.append(("Generator", True))
        else:
            print("✗ Generator not initialized")
            tests.append(("Generator", False))
    except Exception as e:
        print(f"✗ Generator test failed: {e}")
        tests.append(("Generator", False))
    
    # Test 4: Start script
    try:
        from start_api import main
        print("✓ Start script imported")
        tests.append(("Start Script", True))
    except Exception as e:
        print(f"✗ Start script import failed: {e}")
        tests.append(("Start Script", False))
    
    # Test 5: Template
    try:
        if generator and hasattr(generator, 'template'):
            template_content = generator.template.render(
                current_date="2025",
                facture_number="TEST-001",
                date="23/08/2025",
                valid_until="31/08/2025",
                client={"first_name": "Test", "last_name": "Client", "location": "Test"},
                items=[],
                subtotal=0,
                tps=0,
                tvq=0,
                grand_total=0,
                status="A_PAYER"
            )
            print(f"✓ Template rendering works ({len(template_content)} chars)")
            tests.append(("Template", True))
        else:
            print("✗ Template test failed")
            tests.append(("Template", False))
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        tests.append(("Template", False))
    
    # Results summary
    print("\n" + "=" * 40)
    print("Test Results:")
    print("=" * 40)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All components are ready! You can start the API with:")
        print("  python3 start_api.py")
        print("  or")
        print("  ./start_flask.sh")
        return True
    else:
        print("❌ Some components failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)
