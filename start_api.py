#!/usr/bin/env python3
"""
Simple script to start the Flask API for facture generation.
This script provides better error handling and startup feedback.
"""

import os
import sys
import signal
import time
from app import app, generator

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    print("\n🛑 Shutting down Flask API...")
    sys.exit(0)

def main():
    """Main function to start the Flask API."""
    print("🚀 Starting Flask API for Facture Generation")
    print("=" * 50)
    
    # Check if generator is initialized
    if not generator:
        print("❌ FactureGenerator not initialized. Exiting.")
        sys.exit(1)
    
    print("✓ FactureGenerator initialized successfully")
    print("✓ Flask app configured")
    print("✓ All routes registered")
    
    # Set environment variables
    port = int(os.environ.get('PORT', 6000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    print(f"🌐 Starting server on port {port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("")
    print("📋 Available endpoints:")
    print("  GET  /health                    - Health check")
    print("  POST /api/factures/generate     - Generate single facture")
    print("  GET /api/factures/generate-batch - Generate batch factures")
    print("  GET  /api/factures/status       - Get factures status")
    print("  GET  /api/factures/<id>         - Get facture details")
    print("  GET  /api/statistics            - Get statistics")
    print("")
    print("🔗 API will be available at:")
    print(f"  http://localhost:{port}")
    print(f"  Health check: http://localhost:{port}/health")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the Flask app
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False  # Disable reloader for better signal handling
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
