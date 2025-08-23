#!/usr/bin/env python3
"""
Simple test for Flask app without starting the server.
Tests the app configuration and basic functionality.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_flask_app():
    """Test Flask app configuration and basic functionality."""
    print("Testing Flask App Configuration")
    print("=" * 40)
    
    try:
        # Import the app
        from app import app, generator
        
        print("✓ Flask app imported successfully")
        print(f"✓ App name: {app.name}")
        print(f"✓ Generator initialized: {generator is not None}")
        
        # Test app configuration
        print(f"✓ Debug mode: {app.debug}")
        print(f"✓ Testing mode: {app.testing}")
        
        # Test routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        
        print(f"✓ Total routes: {len(routes)}")
        for route in routes:
            if route['endpoint'] != 'static':
                print(f"  - {route['methods']} {route['rule']} -> {route['endpoint']}")
        
        # Test generator functionality
        if generator:
            try:
                # Test config loading
                config = generator.config
                print(f"✓ Generator config loaded: {list(config.keys())}")
                
                # Test template loading
                template = generator.template
                print(f"✓ Template loaded: {template is not None}")
                
            except Exception as e:
                print(f"✗ Generator test failed: {e}")
                return False
        
        print("\n🎉 Flask app configuration test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_flask_app()
    sys.exit(0 if success else 1)
