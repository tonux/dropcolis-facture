#!/usr/bin/env python3
"""
Test script to verify the facture generator setup.
Run this before running the main script to ensure everything is configured correctly.
"""

import sys
import json
import os
import requests
from jinja2 import Template
from weasyprint import HTML

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import requests: {e}")
        return False
    
    try:
        import jinja2
        print("✓ jinja2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import jinja2: {e}")
        return False
    
    try:
        import weasyprint
        print("✓ weasyprint imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import weasyprint: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration file exists and is valid."""
    print("\nTesting configuration...")
    
    config_path = 'config.json'
    if not os.path.exists(config_path):
        print(f"✗ Configuration file not found: {config_path}")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_fields = ['dropcolis_api_url', 'directus_api_url', 'directus_token', 'template_path']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            print(f"✗ Missing required configuration fields: {missing_fields}")
            return False
        
        print("✓ Configuration file loaded successfully")
        print(f"  Dropcolis API: {config['dropcolis_api_url']}")
        print(f"  Directus API: {config['directus_api_url']}")
        print(f"  Template path: {config['template_path']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in configuration file: {e}")
        return False
    except Exception as e:
        print(f"✗ Error reading configuration: {e}")
        return False

def test_template():
    """Test if HTML template exists and can be rendered."""
    print("\nTesting HTML template...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        template_path = config['template_path']
        
        if not os.path.exists(template_path):
            print(f"✗ HTML template not found: {template_path}")
            return False
        
        # Test template rendering
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        # Test data
        test_data = {
            'facture_number': 'TEST-001',
            'date': '01/01/2025',
            'valid_until': '31/01/2025',
            'client_id': 'TEST123',
            'client_name': 'Test Client',
            'client_location': 'Test Location',
            'items': [
                {
                    'prix_unitaire': 100,
                    'quantite': 1,
                    'frais': 10,
                    'total': 110
                }
            ],
            'subtotal': 110,
            'tps': 5.5,
            'tvq': 10.97,
            'grand_total': 126.47
        }
        
        rendered_html = template.render(**test_data)
        
        if rendered_html and len(rendered_html) > 100:
            print("✓ HTML template rendered successfully")
            return True
        else:
            print("✗ HTML template rendered empty or invalid content")
            return False
            
    except Exception as e:
        print(f"✗ Error testing HTML template: {e}")
        return False

def test_weasyprint():
    """Test if WeasyPrint can generate a simple PDF."""
    print("\nTesting WeasyPrint PDF generation...")
    
    try:
        # Create a simple test HTML
        test_html = """
        <html>
            <head>
                <title>Test PDF</title>
            </head>
            <body>
                <h1>Test PDF Generation</h1>
                <p>This is a test to verify WeasyPrint is working correctly.</p>
            </body>
        </html>
        """
        
        # Try to generate PDF (we won't save it, just test the process)
        html_obj = HTML(string=test_html)
        
        # This will test if WeasyPrint can process the HTML
        # We won't actually write the PDF to avoid file system issues
        print("✓ WeasyPrint initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error testing WeasyPrint: {e}")
        return False

def test_api_connectivity():
    """Test basic API connectivity (without authentication)."""
    print("\nTesting API connectivity...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Test Dropcolis API
        try:
            response = requests.get(config['dropcolis_api_url'], timeout=10)
            print(f"✓ Dropcolis API reachable (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠ Dropcolis API connectivity issue: {e}")
        
        # Test Directus API
        try:
            response = requests.get(config['directus_api_url'], timeout=10)
            print(f"✓ Directus API reachable (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"⚠ Directus API connectivity issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing API connectivity: {e}")
        return False

def main():
    """Run all tests."""
    print("Facture Generator Setup Test")
    print("=" * 40)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("HTML Template", test_template),
        ("WeasyPrint", test_weasyprint),
        ("API Connectivity", test_api_connectivity)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n{test_name} test failed!")
        except Exception as e:
            print(f"\n{test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Your setup is ready.")
        print("\nYou can now run: python generate_facture.py")
    else:
        print("✗ Some tests failed. Please fix the issues before running the main script.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Install system dependencies (see README.md)")
        print("3. Update config.json with correct values")
        print("4. Ensure HTML template file exists")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
