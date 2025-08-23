#!/usr/bin/env python3
"""
Test script to generate a sample PDF and verify the visual output.
"""

import sys
import os
import tempfile
from datetime import datetime

# Add the current directory to Python path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_facture import FactureGenerator

def test_pdf_generation():
    """Test PDF generation with sample data."""
    
    print("Testing PDF Generation")
    print("=" * 40)
    
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
        "template_path": "facture_template.html"
    }
    
    try:
        # Initialize the generator
        generator = FactureGenerator(config)
        
        # Get the first facture
        facture_data = api_response['data'][0]
        
        print(f"Generating PDF for facture: {facture_data.get('id')}")
        print(f"Client: {facture_data.get('client', {}).get('first_name')}")
        
        # Generate PDF
        pdf_path = generator.generate_pdf(facture_data)
        
        if pdf_path and os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✓ PDF generated successfully!")
            print(f"  File path: {pdf_path}")
            print(f"  File size: {file_size} bytes")
            
            # Clean up the temporary file
            generator.cleanup_temp_file(pdf_path)
            print(f"  Temporary file cleaned up")
            
            return True
        else:
            print("✗ PDF generation failed")
            return False
        
    except Exception as e:
        print(f"✗ Error during PDF generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    
    if success:
        print("\n🎉 PDF generation test completed successfully!")
        print("The facture template is working correctly and generating PDFs.")
    else:
        print("\n❌ PDF generation test failed. Please review the issues above.")
    
    sys.exit(0 if success else 1)
