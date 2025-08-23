#!/bin/bash

# Docker Deployment Script for Flask API
# This script builds and deploys the Flask API using Docker

set -e

echo "🐳 Docker Deployment for Flask API"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

# Check if config.json exists
check_config() {
    if [ ! -f "config.json" ]; then
        print_error "config.json not found. Please create it first."
        exit 1
    fi
    
    print_success "Configuration file found"
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    
    if docker build -t facture-api:latest .; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Create SSL directory and self-signed certificate (for development)
setup_ssl() {
    if [ ! -d "ssl" ]; then
        print_status "Creating SSL directory and self-signed certificate..."
        mkdir -p ssl
        
        # Generate self-signed certificate
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=CA/ST=QC/L=Montreal/O=ROPCOLIS/CN=localhost"
        
        print_success "SSL certificate created"
    else
        print_status "SSL directory already exists"
    fi
}

# Start services
start_services() {
    print_status "Starting services with Docker Compose..."
    
    if docker-compose up -d; then
        print_success "Services started successfully"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait for services to be ready
    sleep 10
    
    # Check Flask API health
    if curl -f http://localhost:6000/health &> /dev/null; then
        print_success "Flask API is healthy"
    else
        print_warning "Flask API health check failed"
    fi
    
    # Check nginx
    if curl -f http://localhost:80 &> /dev/null; then
        print_success "Nginx is running"
    else
        print_warning "Nginx health check failed"
    fi
}

# Show service status
show_status() {
    print_status "Service status:"
    docker-compose ps
    
    echo ""
    print_status "API endpoints:"
    echo "  HTTP:  http://localhost:80 (redirects to HTTPS)"
    echo "  HTTPS: https://localhost:443"
    echo "  API:   https://localhost:443/api/"
    echo "  Health: https://localhost:443/health"
    echo ""
    print_status "Direct API access:"
    echo "  http://localhost:6000"
    echo "  http://localhost:6000/health"
}

# Stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f
    print_success "Cleanup completed"
}

# Show logs
show_logs() {
    print_status "Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# Main menu
show_menu() {
    echo ""
    echo "🔧 Available commands:"
    echo "  1) build    - Build Docker image"
    echo "  2) start    - Start all services"
    echo "  3) stop     - Stop all services"
    echo "  4) restart  - Restart all services"
    echo "  5) status   - Show service status"
    echo "  6) logs     - Show service logs"
    echo "  7) cleanup  - Clean up Docker resources"
    echo "  8) deploy   - Full deployment (build + start)"
    echo "  9) help     - Show this menu"
    echo "  0) exit     - Exit"
    echo ""
}

# Main function
main() {
    case "${1:-}" in
        "build")
            check_docker
            check_config
            build_image
            ;;
        "start")
            check_docker
            check_config
            setup_ssl
            start_services
            check_health
            show_status
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            start_services
            check_health
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "cleanup")
            cleanup
            ;;
        "deploy")
            check_docker
            check_config
            build_image
            setup_ssl
            start_services
            check_health
            show_status
            ;;
        "help"|"")
            show_menu
            ;;
        "exit"|"0")
            print_status "Exiting..."
            exit 0
            ;;
        *)
            print_error "Unknown command: $1"
            show_menu
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
