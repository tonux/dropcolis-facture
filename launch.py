#!/usr/bin/env python3
"""
Launcher script for the Facture Generation application.
This script provides different launch options for development and production.
"""

import sys
import os
import argparse
import subprocess

def launch_api():
    """Launch the Flask API."""
    print("🚀 Launching Flask API...")
    from src.api.start_api import main
    main()

def launch_docker():
    """Launch using Docker."""
    print("🐳 Launching with Docker...")
    script_path = os.path.join("docker", "scripts", "docker-deploy.sh")
    if os.path.exists(script_path):
        subprocess.run([script_path, "deploy"])
    else:
        print("❌ Docker deployment script not found")
        sys.exit(1)

def launch_tests():
    """Run tests."""
    print("🧪 Running tests...")
    test_dir = os.path.join("tests")
    if os.path.exists(test_dir):
        # Run all test files
        for test_file in os.listdir(test_dir):
            if test_file.startswith("test_") and test_file.endswith(".py"):
                test_path = os.path.join(test_dir, test_file)
                print(f"Running {test_file}...")
                subprocess.run([sys.executable, test_path])
    else:
        print("❌ Tests directory not found")
        sys.exit(1)

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(description="Facture Generation Launcher")
    parser.add_argument(
        "mode",
        choices=["api", "docker", "tests"],
        help="Launch mode: api (Flask), docker (Docker), or tests"
    )
    
    args = parser.parse_args()
    
    # Add src to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    if args.mode == "api":
        launch_api()
    elif args.mode == "docker":
        launch_docker()
    elif args.mode == "tests":
        launch_tests()

if __name__ == "__main__":
    main()
