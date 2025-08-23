#!/usr/bin/env python3
"""
Flask API for Facture Generation
Provides REST endpoints to generate factures and get statistics.
"""

from flask import Flask, request, jsonify, send_file
import os
import tempfile
import logging
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.generate_facture import FactureGenerator, load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global generator instance
generator = None

def initialize_generator():
    """Initialize the FactureGenerator with configuration."""
    global generator
    try:
        config = load_config()
        generator = FactureGenerator(config)
        logger.info("FactureGenerator initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize FactureGenerator: {e}")
        return False

# Initialize generator on import
if not initialize_generator():
    logger.error("Failed to initialize generator during import")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'generator_initialized': generator is not None
    })

@app.route('/api/factures/generate', methods=['POST'])
def generate_facture():
    """
    Generate a single facture PDF.
    
    Expected JSON payload:
    {
        "facture_id": "123",
        "client": {
            "first_name": "John",
            "last_name": "Doe",
            "location": "Montreal"
        },
        "items": [
            {
                "prix_unitaire": 25.0,
                "quantite": 2,
                "frais": 5.0
            }
        ],
        "date_emission": "2025-08-23T12:00:00",
        "date_validite": "2025-08-31T12:00:00",
        "status": "A_PAYER"
    }
    """
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['facture_id', 'client', 'items', 'date_emission', 'date_validite', 'status']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Create facture data structure
        facture_data = {
            'id': data['facture_id'],
            'status': data['status'],
            'date_emission': data['date_emission'],
            'date_validite': data['date_validite'],
            'client': data['client'],
            'lignes': data['items']
        }
        
        # Generate PDF
        result = generator.generate_pdf(facture_data)
        
        if not result:
            return jsonify({'error': 'Failed to generate PDF'}), 500
        
        pdf_path, grand_total, subtotal = result
        
        # Return PDF file
        try:
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"facture_{data['facture_id']}.pdf",
                mimetype='application/pdf'
            )
        finally:
            # Clean up temporary file
            generator.cleanup_temp_file(pdf_path)
            
    except Exception as e:
        logger.error(f"Error generating facture: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/factures/generate-batch/<id>', methods=['GET'])
def generate_factures_batch(id):
    """
    Generate a single facture by ID.
    
    URL parameter:
    - id: The facture ID to process
    """
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        # Process single facture by ID
        stats = generator.process_factures(id)
        
        return jsonify({
            'message': f'Facture {id} processed successfully',
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in facture generation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/factures/generate-batch', methods=['GET'])
def generate_factures_batch_all():
    """
    Generate all factures in batch mode.
    """
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        # Process all factures
        stats = generator.process_factures()
        
        return jsonify({
            'message': 'Batch processing completed',
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in batch generation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/factures/status', methods=['GET'])
def get_factures_status():
    """Get status of factures from the API."""
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        factures = generator.retrieve_factures()
        
        # Format response
        formatted_factures = []
        for facture in factures:
            formatted_factures.append({
                'id': facture.get('id'),
                'status': facture.get('status'),
                'client_name': facture.get('client', {}).get('first_name'),
                'date_emission': facture.get('date_emission'),
                'date_validite': facture.get('date_validite'),
                'montant': facture.get('montant'),
                'montant_ttc': facture.get('montant_ttc')
            })
        
        return jsonify({
            'factures': formatted_factures,
            'total_count': len(formatted_factures),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error retrieving factures status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/factures/<facture_id>', methods=['GET'])
def get_facture_details(facture_id):
    """Get details of a specific facture."""
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        factures = generator.retrieve_factures()
        
        # Find specific facture
        facture = None
        for f in factures:
            if f.get('id') == facture_id:
                facture = f
                break
        
        if not facture:
            return jsonify({'error': 'Facture not found'}), 404
        
        return jsonify({
            'facture': facture,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error retrieving facture details: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get processing statistics."""
    if not generator:
        return jsonify({'error': 'Generator not initialized'}), 500
    
    try:
        # Get current factures
        factures = generator.retrieve_factures()
        
        # Calculate statistics
        status_counts = {}
        total_amount = 0
        total_amount_ttc = 0
        
        for facture in factures:
            status = facture.get('status', 'UNKNOWN')
            status_counts[status] = status_counts.get(status, 0) + 1
            
            montant = facture.get('montant', 0)
            montant_ttc = facture.get('montant_ttc', 0)
            
            if isinstance(montant, (int, float)):
                total_amount += montant
            if isinstance(montant_ttc, (int, float)):
                total_amount_ttc += montant_ttc
        
        return jsonify({
            'total_factures': len(factures),
            'status_distribution': status_counts,
            'total_amount': total_amount,
            'total_amount_ttc': total_amount_ttc,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize generator on startup
    if initialize_generator():
        logger.info("Starting Flask application...")
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=os.environ.get('FLASK_ENV') == 'development'
        )
    else:
        logger.error("Failed to initialize generator. Exiting.")
        exit(1)
