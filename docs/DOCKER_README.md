# 🐳 Docker Deployment for Flask API

This guide explains how to deploy the Flask API using Docker and Docker Compose.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- OpenSSL (for SSL certificates)

## 🚀 Quick Start

### 1. Build and Deploy Everything
```bash
./docker-deploy.sh deploy
```

This command will:
- Build the Docker image
- Create SSL certificates
- Start all services
- Check service health
- Show service status

### 2. Manual Step-by-Step Deployment
```bash
# Build the image
./docker-deploy.sh build

# Start services
./docker-deploy.sh start

# Check status
./docker-deploy.sh status
```

## 🏗️ Architecture

The Docker setup includes:

- **Flask API Container**: Runs the facture generation API on port 6000
- **Nginx Container**: Reverse proxy with SSL termination on ports 80/443
- **Network**: Isolated bridge network for container communication
- **Volumes**: Persistent storage for logs and configuration

## 📁 File Structure

```
generate_facture/
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Service orchestration
├── nginx.conf             # Nginx configuration
├── docker-deploy.sh       # Deployment script
├── .dockerignore          # Docker build exclusions
└── DOCKER_README.md       # This file
```

## 🔧 Configuration

### Environment Variables

The following environment variables can be customized:

```bash
# Flask API
FLASK_ENV=production
FLASK_DEBUG=0
PORT=6000
API_HOST=0.0.0.0
API_TIMEOUT=30
LOG_LEVEL=INFO

# Docker Compose
COMPOSE_PROJECT_NAME=facture-api
```

### SSL Configuration

For production, replace the self-signed certificates in the `ssl/` directory with your own:

```bash
# Your certificates should be named:
ssl/cert.pem    # SSL certificate
ssl/key.pem     # Private key
```

## 🚀 Deployment Commands

### Available Commands

```bash
./docker-deploy.sh [command]

Commands:
  build     - Build Docker image
  start     - Start all services
  stop      - Stop all services
  restart   - Restart all services
  status    - Show service status
  logs      - Show service logs
  cleanup   - Clean up Docker resources
  deploy    - Full deployment (build + start)
  help      - Show this menu
```

### Service Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f flask-api

# Restart specific service
docker-compose restart flask-api
```

## 🌐 Access Points

After deployment, the API is available at:

| Service | URL | Description |
|---------|-----|-------------|
| **Nginx (HTTP)** | http://localhost:80 | Redirects to HTTPS |
| **Nginx (HTTPS)** | https://localhost:443 | Main API gateway |
| **Flask API** | http://localhost:6000 | Direct API access |
| **Health Check** | https://localhost:443/health | Service health |

## 📊 Monitoring

### Health Checks

The containers include health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:6000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Logs

View logs for different services:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f flask-api
docker-compose logs -f nginx

# Follow logs in real-time
docker-compose logs -f --tail=100
```

## 🔒 Security Features

### Nginx Security Headers

```nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ {
    limit_req zone=api burst=20 nodelay;
}
```

### SSL/TLS Configuration

- TLS 1.2 and 1.3 support
- Strong cipher suites
- HSTS headers
- Automatic HTTP to HTTPS redirect

## 🧪 Testing

### Test the API

```bash
# Health check
curl -k https://localhost/health

# Generate a facture
curl -k -X POST https://localhost/api/factures/generate \
  -H "Content-Type: application/json" \
  -d '{
    "facture_id": "TEST-001",
    "client": {
      "first_name": "Test Client",
      "location": "Montreal, QC"
    },
    "items": [
      {
        "prix_unitaire": 25.0,
        "quantite": 2,
        "frais": 5.0
      }
    ],
    "date_emission": "2025-08-23T12:00:00",
    "date_service": "2025-09-22T12:00:00",
    "status": "A_PAYER"
  }' \
  --output facture_test.pdf
```

### Test Individual Services

```bash
# Test Flask API directly
curl http://localhost:6000/health

# Test Nginx
curl -k https://localhost/health
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
lsof -i :6000
lsof -i :80
lsof -i :443

# Stop conflicting services or change ports in docker-compose.yml
```

#### 2. SSL Certificate Issues
```bash
# Regenerate self-signed certificates
rm -rf ssl/
./docker-deploy.sh start
```

#### 3. Permission Issues
```bash
# Fix file permissions
chmod +x docker-deploy.sh
chmod 644 config.json
```

#### 4. Container Won't Start
```bash
# Check container logs
docker-compose logs flask-api

# Check container status
docker-compose ps

# Restart services
docker-compose restart
```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Edit docker-compose.yml
environment:
  - FLASK_DEBUG=1
  - LOG_LEVEL=DEBUG

# Restart services
docker-compose restart
```

## 📈 Performance Tuning

### Nginx Optimization

```nginx
# Gzip compression
gzip on;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript;

# Buffer settings
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
```

### Docker Optimization

```yaml
# Resource limits
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
    reservations:
      memory: 256M
      cpus: '0.25'
```

## 🚀 Production Deployment

### 1. Update Configuration

```bash
# Edit config.json with production values
{
  "dropcolis_api_url": "https://production-api.dropcolis.ca",
  "directus_api_url": "https://production-directus.dropcolis.ca",
  "directus_token": "your-production-token"
}
```

### 2. SSL Certificates

```bash
# Replace self-signed certificates with production ones
cp /path/to/production/cert.pem ssl/cert.pem
cp /path/to/production/key.pem ssl/key.pem
```

### 3. Environment Variables

```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=0
export LOG_LEVEL=WARNING
```

### 4. Deploy

```bash
./docker-deploy.sh deploy
```

## 🔄 Updates and Maintenance

### Update the Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
./docker-deploy.sh deploy
```

### Backup Configuration

```bash
# Backup important files
cp config.json config.json.backup
cp -r ssl/ ssl.backup/
```

### Clean Up

```bash
# Remove old images and containers
./docker-deploy.sh cleanup

# Or manually
docker system prune -a
docker volume prune
```

## 📚 Additional Resources

### Docker Commands Reference

```bash
# Container management
docker ps -a                    # List all containers
docker images                   # List images
docker logs <container_id>      # View container logs
docker exec -it <container_id> bash  # Access container shell

# Docker Compose
docker-compose config           # Validate configuration
docker-compose pull            # Pull latest images
docker-compose build --no-cache # Force rebuild
```

### Useful Scripts

```bash
# Quick health check
curl -f http://localhost:6000/health && echo "API OK" || echo "API DOWN"

# Monitor resource usage
docker stats

# Check disk usage
docker system df
```

---

## 🎯 Next Steps

1. **Customize Configuration**: Update `config.json` with your API endpoints
2. **SSL Certificates**: Replace self-signed certificates with production ones
3. **Monitoring**: Set up log aggregation and monitoring
4. **Backup**: Implement backup strategies for configuration and data
5. **Scaling**: Consider horizontal scaling with multiple API instances

---

**🐳 Your Flask API is now containerized and ready for production deployment!**

For support, check the logs with `./docker-deploy.sh logs` or run `./docker-deploy.sh help` for available commands.
