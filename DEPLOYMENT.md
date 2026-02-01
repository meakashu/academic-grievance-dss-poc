# Deployment Guide - Academic Grievance DSS

## Overview

This guide covers deploying the Academic Grievance DSS in different environments.

---

## Quick Deployment (Development)

### Prerequisites
- Python 3.9+
- (Optional) Node.js 16+
- (Optional) Docker

### Steps

**1. Clone/Navigate to Project**
```bash
cd /Volumes/Winner/research\ work/all\ paper/academic-grievance-dss-poc
```

**2. Start Backend**
```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Verify Backend**
```bash
curl http://localhost:8000/health
```

**4. (Optional) Start Frontend**
```bash
cd frontend
npm install
npm start
```

**Done!** Backend is at http://localhost:8000, Frontend at http://localhost:3000

---

## Production Deployment

### Option 1: Docker Compose (Recommended)

**1. Install Docker**
```bash
# macOS
brew install docker docker-compose

# Or download Docker Desktop
```

**2. Configure Environment**
```bash
# Edit backend/.env for production settings
cp backend/.env.example backend/.env
nano backend/.env
```

**3. Deploy with Docker Compose**
```bash
docker-compose up -d
```

**4. Verify Deployment**
```bash
curl http://localhost:8000/health
```

**5. View Logs**
```bash
docker-compose logs -f
```

**6. Stop Services**
```bash
docker-compose down
```

---

### Option 2: Manual Production Deployment

#### Backend Deployment

**1. Install Dependencies**
```bash
cd backend
pip3 install -r requirements.txt
```

**2. Configure Production Settings**
```bash
# backend/.env
DEBUG_MODE=False
LOG_LEVEL=WARNING
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

**3. Start with Gunicorn**
```bash
pip3 install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**4. (Optional) Use Supervisor**
```bash
# Install supervisor
pip3 install supervisor

# Create config: /etc/supervisor/conf.d/grievance-dss.conf
[program:grievance-dss]
command=/usr/local/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/grievance-dss.err.log
stdout_logfile=/var/log/grievance-dss.out.log

# Start
supervisorctl reread
supervisorctl update
supervisorctl start grievance-dss
```

#### Frontend Deployment

**1. Build Production Bundle**
```bash
cd frontend
npm install
npm run build
```

**2. Serve with Nginx**
```bash
# Install nginx
brew install nginx

# Configure: /usr/local/etc/nginx/nginx.conf
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/frontend/build;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Start nginx
nginx
```

---

### Option 3: Cloud Deployment

#### AWS Deployment

**1. Backend on EC2**
```bash
# Launch EC2 instance (Ubuntu 22.04)
# SSH into instance
ssh -i key.pem ubuntu@ec2-instance

# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone project
git clone your-repo
cd academic-grievance-dss-poc/backend

# Install Python packages
pip3 install -r requirements.txt

# Start with systemd
sudo nano /etc/systemd/system/grievance-dss.service
```

**systemd service file:**
```ini
[Unit]
Description=Grievance DSS API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/academic-grievance-dss-poc/backend
ExecStart=/usr/local/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable grievance-dss
sudo systemctl start grievance-dss
```

**2. Frontend on S3 + CloudFront**
```bash
# Build frontend
cd frontend
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name/

# Configure CloudFront distribution
# Point to S3 bucket
# Enable HTTPS
```

**3. Database on RDS**
```bash
# Create PostgreSQL RDS instance
# Update backend/.env with RDS endpoint
POSTGRES_HOST=your-rds-endpoint.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DB=grievance_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=your-password
```

#### Heroku Deployment

**1. Install Heroku CLI**
```bash
brew install heroku/brew/heroku
heroku login
```

**2. Create Heroku App**
```bash
cd backend
heroku create grievance-dss-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git init
heroku git:remote -a grievance-dss-api
git add .
git commit -m "Initial deployment"
git push heroku main
```

**3. Configure Environment**
```bash
heroku config:set DEBUG_MODE=False
heroku config:set LOG_LEVEL=WARNING
```

---

## Database Setup

### PostgreSQL (Production)

**1. Install PostgreSQL**
```bash
# macOS
brew install postgresql@15

# Ubuntu
sudo apt install postgresql-15
```

**2. Create Database**
```bash
# Start PostgreSQL
brew services start postgresql@15

# Create database
createdb grievance_db

# Create user
psql -d grievance_db
CREATE USER grievance_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE grievance_db TO grievance_user;
```

**3. Initialize Schema**
```bash
psql -U grievance_user -d grievance_db -f database/init.sql
```

**4. (Optional) Load Sample Data**
```bash
psql -U grievance_user -d grievance_db -f database/seed.sql
```

**5. Update Backend Configuration**
```bash
# backend/.env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=grievance_db
POSTGRES_USER=grievance_user
POSTGRES_PASSWORD=your-password
```

---

## Rule Engine Setup

### Drools (Optional)

**1. Install Java and Maven**
```bash
# macOS
brew install openjdk@11 maven

# Ubuntu
sudo apt install openjdk-11-jdk maven
```

**2. Build Drools JAR**
```bash
cd java-bridge
mvn clean package

# JAR will be in target/grievance-rule-engine-1.0.jar
```

**3. Install JPype1**
```bash
pip3 install JPype1
```

**4. Update Backend Configuration**
```bash
# backend/.env
DROOLS_JAR_PATH=/path/to/java-bridge/target/grievance-rule-engine-1.0.jar
DROOLS_RULES_PATH=/path/to/rules
```

---

## Monitoring & Logging

### Application Logs

**Backend Logs**
```bash
# Development
# Logs appear in terminal running uvicorn

# Production (with gunicorn)
tail -f /var/log/grievance-dss.out.log
tail -f /var/log/grievance-dss.err.log
```

### Health Monitoring

**1. Health Check Endpoint**
```bash
curl http://localhost:8000/health
```

**2. Automated Monitoring**
```bash
# Add to cron
*/5 * * * * curl -f http://localhost:8000/health || echo "API Down" | mail -s "Alert" admin@example.com
```

**3. Application Metrics**
```bash
# Install Prometheus (optional)
brew install prometheus

# Configure backend to export metrics
# Add prometheus_client to requirements.txt
```

---

## Security Considerations

### 1. Environment Variables
```bash
# Never commit .env files
# Use environment-specific .env files
# Rotate secrets regularly
```

### 2. HTTPS
```bash
# Use Let's Encrypt for SSL
sudo certbot --nginx -d your-domain.com
```

### 3. API Authentication
```bash
# Add API key authentication (future enhancement)
# Implement JWT tokens
# Rate limiting
```

### 4. Database Security
```bash
# Use strong passwords
# Enable SSL for database connections
# Restrict database access by IP
```

---

## Scaling

### Horizontal Scaling

**1. Load Balancer**
```bash
# Nginx load balancer config
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

**2. Multiple Backend Instances**
```bash
# Start multiple instances on different ports
gunicorn main:app --bind 0.0.0.0:8001
gunicorn main:app --bind 0.0.0.0:8002
gunicorn main:app --bind 0.0.0.0:8003
```

### Vertical Scaling

**Increase Workers**
```bash
# More workers for more CPU cores
gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker
```

---

## Backup & Recovery

### Database Backup

**1. Automated Backups**
```bash
# Create backup script: backup.sh
#!/bin/bash
pg_dump -U grievance_user grievance_db > backup_$(date +%Y%m%d).sql
aws s3 cp backup_$(date +%Y%m%d).sql s3://backups/

# Add to cron
0 2 * * * /path/to/backup.sh
```

**2. Restore from Backup**
```bash
psql -U grievance_user -d grievance_db < backup_20260201.sql
```

---

## Testing Deployment

### 1. Health Check
```bash
curl http://your-domain.com/health
```

### 2. API Test
```bash
curl -X POST http://your-domain.com/api/grievances \
  -H "Content-Type: application/json" \
  -d @test_grievance.json
```

### 3. Load Testing
```bash
# Install Apache Bench
brew install httpd

# Run load test
ab -n 1000 -c 10 http://localhost:8000/health
```

---

## Rollback Procedure

**1. Stop Current Version**
```bash
sudo systemctl stop grievance-dss
```

**2. Restore Previous Version**
```bash
git checkout previous-tag
pip3 install -r requirements.txt
```

**3. Restart Service**
```bash
sudo systemctl start grievance-dss
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Check health endpoint
- Review error logs
- Monitor disk space

**Weekly:**
- Database backup verification
- Security updates
- Performance review

**Monthly:**
- Dependency updates
- Security audit
- Capacity planning

---

## Quick Reference

**Start Development:**
```bash
cd backend && python3 -m uvicorn main:app --reload
```

**Start Production:**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Check Status:**
```bash
curl http://localhost:8000/health
```

**View Logs:**
```bash
tail -f /var/log/grievance-dss.out.log
```

**Restart Service:**
```bash
sudo systemctl restart grievance-dss
```

---

**For detailed troubleshooting, see TROUBLESHOOTING.md**
