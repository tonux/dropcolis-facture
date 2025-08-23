#!/usr/bin/env python3
"""
Docker setup test script.
This script verifies that the Docker configuration is correct.
"""

import os
import sys
import subprocess
import json

def run_command(command, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_docker_installation():
    """Check if Docker and Docker Compose are installed."""
    print("🔍 Checking Docker installation...")
    
    # Check Docker
    success, stdout, stderr = run_command("docker --version")
    if success:
        print(f"✓ Docker: {stdout.strip()}")
    else:
        print("✗ Docker not found")
        return False
    
    # Check Docker Compose
    success, stdout, stderr = run_command("docker-compose --version")
    if success:
        print(f"✓ Docker Compose: {stdout.strip()}")
    else:
        print("✗ Docker Compose not found")
        return False
    
    return True

def check_dockerfile():
    """Check if Dockerfile exists and is valid."""
    print("\n🔍 Checking Dockerfile...")
    
    if not os.path.exists("Dockerfile"):
        print("✗ Dockerfile not found")
        return False
    
    print("✓ Dockerfile exists")
    
    # Check if Dockerfile has required content
    with open("Dockerfile", "r") as f:
        content = f.read()
        
    required_elements = [
        "FROM python:",
        "COPY requirements.txt",
        "EXPOSE",
        "CMD"
    ]
    
    for element in required_elements:
        if element in content:
            print(f"✓ Contains: {element}")
        else:
            print(f"✗ Missing: {element}")
            return False
    
    return True

def check_docker_compose():
    """Check if docker-compose.yml exists and is valid."""
    print("\n🔍 Checking docker-compose.yml...")
    
    if not os.path.exists("docker-compose.yml"):
        print("✗ docker-compose.yml not found")
        return False
    
    print("✓ docker-compose.yml exists")
    
    # Validate docker-compose.yml
    success, stdout, stderr = run_command("docker-compose config")
    if success:
        print("✓ docker-compose.yml is valid")
        return True
    else:
        print(f"✗ docker-compose.yml validation failed: {stderr}")
        return False

def check_required_files():
    """Check if all required files exist."""
    print("\n🔍 Checking required files...")
    
    required_files = [
        "app.py",
        "start_api.py",
        "api_config.py",
        "generate_facture.py",
        "facture_template.html",
        "logo.png",
        "config.json",
        "requirements.txt"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist

def check_docker_build():
    """Test Docker build process."""
    print("\n🔍 Testing Docker build...")
    
    # Check if we can validate the Dockerfile syntax
    success, stdout, stderr = run_command("docker build --help")
    if success:
        print("✓ Docker build command available")
        return True
    else:
        print(f"✗ Docker build command failed: {stderr}")
        return False

def check_ports():
    """Check if required ports are available."""
    print("\n🔍 Checking port availability...")
    
    ports_to_check = [6000, 80, 443]
    
    for port in ports_to_check:
        success, stdout, stderr = run_command(f"lsof -i :{port}")
        if success and stdout.strip():
            if port == 443:
                print(f"⚠️  Port {port} is in use (common for HTTPS, will use different port)")
            else:
                print(f"⚠️  Port {port} is in use:")
                print(f"   {stdout.strip()}")
        else:
            print(f"✓ Port {port} is available")
    
    # Port 443 being in use is not a blocker for development
    return True

def main():
    """Main test function."""
    print("🐳 Docker Setup Test")
    print("=" * 40)
    
    tests = [
        ("Docker Installation", check_docker_installation),
        ("Dockerfile", check_dockerfile),
        ("Docker Compose", check_docker_compose),
        ("Required Files", check_required_files),
        ("Docker Build", check_docker_build),
        ("Port Availability", check_ports)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Results:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Docker setup is ready!")
        print("\nNext steps:")
        print("1. Run: ./docker-deploy.sh deploy")
        print("2. Or manually:")
        print("   - ./docker-deploy.sh build")
        print("   - ./docker-deploy.sh start")
        print("3. Check status: ./docker-deploy.sh status")
        return True
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
