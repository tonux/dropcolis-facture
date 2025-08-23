#!/usr/bin/env python3
"""
Main entry point for the Facture Generation API.
This script can be run from the root directory to start the Flask API.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api.start_api import main

if __name__ == "__main__":
    main()
