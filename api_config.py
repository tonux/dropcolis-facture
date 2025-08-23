#!/usr/bin/env python3
"""
Configuration file for Flask API.
Contains all the configuration options and environment variables.
"""

import os
from typing import Dict, Any

class APIConfig:
    """Configuration class for Flask API."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.port = int(os.environ.get('PORT', 5000))
        self.host = os.environ.get('API_HOST', '0.0.0.0')
        self.debug = os.environ.get('FLASK_DEBUG', '0') == '1'
        self.env = os.environ.get('FLASK_ENV', 'development')
        self.timeout = int(os.environ.get('API_TIMEOUT', 30))
        self.log_level = os.environ.get('LOG_LEVEL', 'INFO')
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'port': self.port,
            'host': self.host,
            'debug': self.debug,
            'env': self.env,
            'timeout': self.timeout,
            'log_level': self.log_level
        }
    
    def print_config(self):
        """Print current configuration."""
        print("🔧 API Configuration:")
        print(f"  Port: {self.port}")
        print(f"  Host: {self.host}")
        print(f"  Debug: {'ON' if self.debug else 'OFF'}")
        print(f"  Environment: {self.env}")
        print(f"  Timeout: {self.timeout}s")
        print(f"  Log Level: {self.log_level}")

# Global configuration instance
config = APIConfig()

if __name__ == '__main__':
    config.print_config()
