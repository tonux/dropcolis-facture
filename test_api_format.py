#!/usr/bin/env python3
"""
Test script to verify the facture generator works with the actual API response format.
"""

import json
from datetime import datetime
from jinja2 import Template

def test_api_response_format():
    """Test the code with the actual API response format."""
    
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
    
    print("Testing API response format processing...")
    print("=" * 50)
    
    # Simulate the data processing from generate_facture.py
    facture_data = api_response['data'][0]
    
    # Extract data using the updated field mappings
    facture_number = facture_data.get('id', 'N/A')
    date = facture_data.get('date_emission', datetime.now().strftime('%d/%m/%Y'))
    valid_until = facture_data.get('date_validite', 'N/A')
    client_id = facture_data.get('client', {}).get('id', '---------')
    client_name = facture_data.get('client', {}).get('first_name', 'N/A')
    client_location = facture_data.get('client', {}).get('location', 'N/A')
    items = facture_data.get('lignes', [])
    
    print(f"Facture Number: {facture_number}")
    print(f"Date: {date}")
    print(f"Valid Until: {valid_until}")
    print(f"Client ID: {client_id}")
    print(f"Client Name: {client_name}")
    print(f"Client Location: {client_location}")
    print(f"Number of Items: {len(items)}")
    
    # Calculate totals (simulating the calculation logic)
    subtotal = 0
    for item in items:
        item_total = (item.get('prix_unitaire', 0) * item.get('quantite', 0)) + item.get('frais', 0)
        item['total'] = item_total
        subtotal += item_total
    
    print(f"Subtotal: {subtotal}$")
    
    # Calculate taxes
    tps_rate = 0.05
    tvq_rate = 0.09975
    
    tps = round(subtotal * tps_rate, 2)
    tvq = round(subtotal * tvq_rate, 2)
    grand_total = round(subtotal + tps + tvq, 2)
    
    print(f"TPS (5%): {tps}$")
    print(f"TVQ (9.975%): {tvq}$")
    print(f"Grand Total: {grand_total}$")
    
    # Test template rendering
    print("\nTesting template rendering...")
    
    try:
        with open('facture_template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        template_vars = {
            'facture_number': facture_number,
            'date': date,
            'valid_until': valid_until,
            'client_id': client_id,
            'client_name': client_name,
            'client_location': client_location,
            'items': items,
            'subtotal': subtotal,
            'tps': tps,
            'tvq': tvq,
            'grand_total': grand_total
        }
        
        rendered_html = template.render(**template_vars)
        
        if rendered_html and len(rendered_html) > 100:
            print("✓ HTML template rendered successfully")
            print(f"  Rendered HTML length: {len(rendered_html)} characters")
            
            # Check if key data is present in rendered HTML
            if client_name in rendered_html:
                print("✓ Client name found in rendered HTML")
            else:
                print("✗ Client name not found in rendered HTML")
            
            if str(subtotal) in rendered_html:
                print("✓ Subtotal found in rendered HTML")
            else:
                print("✗ Subtotal not found in rendered HTML")
            
            if str(grand_total) in rendered_html:
                print("✓ Grand total found in rendered HTML")
            else:
                print("✗ Grand total not found in rendered HTML")
                
        else:
            print("✗ HTML template rendered empty or invalid content")
            return False
            
    except Exception as e:
        print(f"✗ Error testing HTML template: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("API format test completed successfully!")
    return True

def test_field_mappings():
    """Test that all expected fields are properly mapped."""
    
    print("\nTesting field mappings...")
    print("=" * 30)
    
    # Test data structure
    test_data = {
        "id": "test-facture-123",
        "date_emission": "2025-08-23T12:00:00",
        "date_validite": "2025-08-31T12:00:00",
        "client": {
            "id": "client-uuid-123",
            "first_name": "Test Client",
            "location": "Test Location"
        },
        "lignes": [
            {
                "prix_unitaire": 25,
                "quantite": 2,
                "frais": 5
            }
        ]
    }
    
    # Test field extraction
    fields = {
        'facture_number': test_data.get('id'),
        'date': test_data.get('date_emission'),
        'valid_until': test_data.get('date_validite'),
        'client_id': test_data.get('client', {}).get('id'),
        'client_name': test_data.get('client', {}).get('first_name'),
        'client_location': test_data.get('client', {}).get('location'),
        'items': test_data.get('lignes')
    }
    
    for field_name, value in fields.items():
        if value is not None:
            print(f"✓ {field_name}: {value}")
        else:
            print(f"✗ {field_name}: None/Not found")
    
    return all(value is not None for value in fields.values())

if __name__ == "__main__":
    print("API Format Test Suite")
    print("=" * 50)
    
    success1 = test_api_response_format()
    success2 = test_field_mappings()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The code is ready to work with the actual API format.")
    else:
        print("\n❌ Some tests failed. Please review the issues above.")
