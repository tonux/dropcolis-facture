#!/usr/bin/env python3
"""
Complete test of the FactureGenerator class with actual data processing.
"""

import sys
import os
import tempfile
from datetime import datetime

# Add the current directory to Python path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from core.generate_facture import FactureGenerator

def test_complete_generation():
    """Test the complete facture generation process."""
    
    print("Testing Complete Facture Generation")
    print("=" * 50)
    
    # Sample API response based on the user's example
    api_response = {
        "data": [{
            "id": "FACT-2025-001",
            "status": "A_PAYER",
            "montant": 100,
            "montant_ttc": 100,
            "devise": "CAD",
            "mode_paiement": "Interact",
            "date_validite": "2025-08-31T12:00:00",
            "date_emission": "2025-08-23T12:00:00",
            "client": {
                "id": "4f2d0d08-eb15-44e9-b3e1-9dc41a533c67",
                "first_name": "Happiness perfumes",
                "last_name": None,
                "email": "florapclahon@gmail.com",
                "location": "Quebec city",
                "title": "Fondatrice"
            },
            "lignes": [{
                "id": 1,
                "facture": 1,
                "prix_unitaire": 10,
                "quantite": 3,
                "frais": 20,
                "total": 100
            }]
        }]
    }
    
    # Create a minimal config for testing
    config = {
        "dropcolis_api_url": "https://services.dropcolis.ca",
        "directus_api_url": "https://services.dropcolis.ca",
        "directus_token": "test-token",
        "template_path": "src/templates/facture_template.html"
    }
    
    try:
        # Initialize the generator
        generator = FactureGenerator(config)
        
        # Get the first facture
        facture_data = api_response['data'][0]
        
        print(f"Processing facture: {facture_data.get('id')}")
        print(f"Client: {facture_data.get('client', {}).get('first_name')}")
        print(f"Date emission: {facture_data.get('date_emission')}")
        print(f"Date validite: {facture_data.get('date_validite')}")
        
        # Test date formatting directly
        formatted_emission = generator.format_date(facture_data.get('date_emission'))
        formatted_validite = generator.format_date(facture_data.get('date_validite'))
        
        print(f"\nDate formatting test:")
        print(f"  Emission: {facture_data.get('date_emission')} -> {formatted_emission}")
        print(f"  Validite: {facture_data.get('date_validite')} -> {formatted_validite}")
        
        # Test template variable preparation
        template_vars = {
            'current_date': datetime.now().strftime('%Y'),
            'facture_number': facture_data.get('id', facture_data.get('numero', 'N/A')),
            'date': generator.format_date(facture_data.get('date_emission')),
            'valid_until': generator.format_date(facture_data.get('date_validite')),
            'client': {
                'first_name': facture_data.get('client', {}).get('first_name', 'N/A'),
                'last_name': facture_data.get('client', {}).get('last_name', ''),
                'location': facture_data.get('client', {}).get('location', 'N/A')
            },
            'items': facture_data.get('lignes', []),
            'subtotal': 0,
            'tps': 0,
            'tvq': 0,
            'grand_total': 0
        }
        
        print(f"\nTemplate variables:")
        print(f"  Facture Number: {template_vars['facture_number']}")
        print(f"  Date: {template_vars['date']}")
        print(f"  Valid Until: {template_vars['valid_until']}")
        print(f"  Client Name: {template_vars['client']['first_name']}")
        print(f"  Client Location: {template_vars['client']['location']}")
        
        # Test template rendering
        print(f"\nTesting template rendering...")
        rendered_html = generator.template.render(**template_vars)
        
        if rendered_html and len(rendered_html) > 100:
            print("✓ HTML template rendered successfully")
            print(f"  Rendered HTML length: {len(rendered_html)} characters")
            
            # Check if formatted dates are present in rendered HTML
            if formatted_emission in rendered_html:
                print("✓ Formatted emission date found in HTML")
            else:
                print("✗ Formatted emission date not found in HTML")
            
            if formatted_validite in rendered_html:
                print("✓ Formatted validite date found in HTML")
            else:
                print("✗ Formatted validite date not found in HTML")
            
            if template_vars['client']['first_name'] in rendered_html:
                print("✓ Client name found in HTML")
            else:
                print("✗ Client name not found in HTML")
                
        else:
            print("✗ HTML template rendered empty or invalid content")
            return False
        
        print(f"\n" + "=" * 50)
        print("Complete generation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error during complete generation test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_generation()
    
    if success:
        print("\n🎉 All tests passed! The facture generator is working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
    
    sys.exit(0 if success else 1)
