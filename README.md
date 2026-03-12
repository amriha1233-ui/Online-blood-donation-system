# OBDMS - Online Blood Bank Management System
## Production Deployment Guide

> **Status**: ✅ Production-Ready | **Python**: 3.11 | **Django**: 5.0+ | **Database**: PostgreSQL

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Production Issues Fixed](#production-issues-fixed)
4. [Deployment Options](#deployment-options)
5. [Local Development](#local-development)
6. [Docker Deployment](#docker-deployment)
7. [Pre-Deployment Checklist](#pre-deployment-checklist)
8. [Troubleshooting](#troubleshooting)
9. [Security](#security)

---

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended - 5 minutes)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Link your project
railway link

# 4. Deploy
railway up
```

### Option 2: Deploy with Docker Compose (Local/VPS)

```bash
# 1. Clone & setup
git clone <your-repo>
cd sanjevnii
cp .env.example .env

# 2. Update .env with your credentials
nano .env

# 3. Start services
docker-compose up -d

# 4. Access application
# http://localhost or http://your-domain
```

### Option 3: Manual Deployment (VPS/EC2)

```bash
# 1. SSH into your server
ssh user@your-server.com

# 2. Install dependencies
sudo apt-get update
sudo apt-get install -y postgresql-client redis-server python3.11 python3.11-venv

# 3. Clone repository
git clone <your-repo>
cd sanjevnii

# 4. Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# 6. Run migrations
python manage.py migrate

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start application with Gunicorn
gunicorn obdms.wsgi --bind 0.0.0.0:8000 --workers 4
```

---

## 📊 Project Overview

**OBDMS** is a Django-based Blood Bank Management System featuring:

- 👥 **Donor Management**: Register, track donation history, blood type
- 🏥 **Hospital Requests**: Create blood requests, track status
- 🩸 **Blood Request Matching**: Auto-match donors with hospital needs
- 📧 **Email Notifications**: Gmail SMTP integration for notifications
- 🔐 **User Authentication**: Separate login for donors and hospitals
- 📊 **Dashboard**: Real-time statistics and analytics

**Key Features**:
- Multi-app Django structure (accounts, donors, hospitals, blood_requests)
- SQLite for development → PostgreSQL for production
- Email-based notifications
- Responsive design with HTML/CSS templates

---

## ✅ Production Issues Fixed

### 🔴 Issues Detected

| Issue | Status | Solution |
|-------|--------|----------|
| SQLite in production | ❌ | ✅ PostgreSQL configured |
| DEBUG=True | ❌ | ✅ Set DEBUG=False in settings |
| No HTTPS settings | ❌ | ✅ Added SSL/TLS config |
| Hardcoded secrets | ⚠️ Partial | ✅ All moved to .env |
| No static files CDN | ⚠️ | ✅ WhiteNoise for static serving |
| No caching | ⚠️ | ✅ Redis configured |
| No error tracking | ⚠️ | ✅ Sentry integration added |
| No CI/CD pipeline | ❌ | ✅ GitHub Actions with auto-deploy |
| No Docker setup | ❌ | ✅ Multi-stage Dockerfile created |
| No load balancing | ⚠️ | ✅ Nginx reverse proxy configured |

### 📁 Files Created/Modified

```
✅ NEW FILES:
├── Dockerfile (production-ready multi-stage)
├── docker-compose.yml (complete stack)
├── .dockerignore (optimized)
├── nginx.conf (reverse proxy)
├── gunicorn.conf.py (WSGI configuration)
├── entrypoint.sh (startup script)
├── .env.example (comprehensive template)
├── obdms/settings_production.py (production settings)
├── .github/workflows/deploy.yml (CI/CD)
├── Procfile (updated for production)
├── railway.json, fly.toml, render.yaml (platform configs)
├── scripts/deploy-railway.sh
├── scripts/deploy-fly.sh
├── scripts/setup-dev.sh
├── scripts/production-startup.sh

✅ MODIFIED FILES:
├── requirements.txt (added production packages)
├── .env.example (comprehensive configuration)
├── Procfile (enhanced)
```

---

## 🌐 Deployment Options

### 1. **Railway** ⭐ (Recommended)
- **Pros**: GitHub integration, automatic deployments, free tier, built-in PostgreSQL
- **Cost**: Free tier available, $5-20/month for production
- **Setup Time**: 5 minutes
- **URL**: https://railway.app
- **Steps**:
  ```bash
  npm install -g @railway/cli
  railway login
  railway link
  railway up
  ```

### 2. **Render**
- **Pros**: Free tier, auto-deploy from GitHub, PostgreSQL included
- **Cost**: Free tier, $12+/month production
- **Setup Time**: 10 minutes
- **URL**: https://render.com
- **Steps**:
  ```bash
  # Connect GitHub repo directly from dashboard
  ```

### 3. **Fly.io**
- **Pros**: Global deployment, great performance, good free tier
- **Cost**: Free tier, $10+/month production
- **Setup Time**: 15 minutes
- **URL**: https://fly.io
- **Steps**:
  ```bash
  brew install flyctl
  flyctl auth login
  flyctl deploy
  ```

### 4. **AWS EC2 / DigitalOcean VPS**
- **Pros**: Full control, scalable, pay-as-you-go
- **Cost**: $5-20/month
- **Setup Time**: 30-60 minutes
- **Deploy Script**: Use `scripts/production-startup.sh`

### 5. **Heroku** (Legacy - Not Recommended)
- **Status**: Free tier removed as of Nov 2022
- **Alternative**: Use Railway/Render instead

---

## 💻 Local Development

### First-Time Setup

```bash
# 1. Clone repository
git clone <your-repo>
cd sanjevnii

# 2. Run setup script
bash scripts/setup-dev.sh

# 3. Create .env for development
cp .env.example .env
# Edit .env, keep DEBUG=True for development

# 4. Start development server
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000

# 5. Access application
# http://localhost:8000
# Admin: http://localhost:8000/admin
```

### With Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down
```

### Development Environment Variables

```bash
# .env (for development)
DEBUG=True
SECRET_KEY=dev-key-not-secure-for-production-only
DATABASE_URL=postgresql://user:pw@localhost:5432/obdms_dev
ALLOWED_HOSTS=localhost,127.0.0.1,127.0.0.1:8000
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379/0
```

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
# Build image
docker build -t obdms:latest .

# Run container
docker run -d \
  --name obdms \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  -e EMAIL_HOST_USER=your-email@gmail.com \
  -e EMAIL_HOST_PASSWORD=your-app-password \
  -p 8000:8000 \
  obdms:latest
```

### Push to Container Registry (for Railway/Render)

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag obdms:latest your-username/obdms:latest

# Push
docker push your-username/obdms:latest
```

### Docker Compose Stack

The `docker-compose.yml` includes:
- **PostgreSQL 15**: Database (port 5432)
- **Redis 7**: Caching (port 6379)
- **Django App**: WSGI server (port 8000)
- **Nginx**: Reverse proxy (port 80)

```bash
# Start all services
docker-compose up -d

# View status
docker-compose ps

# Check logs
docker-compose logs -f

# Stop everything
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

---

## ✅ Pre-Deployment Checklist

### Before Going Live

- [ ] **Environment Variables Set**
  ```bash
  echo $SECRET_KEY
  echo $DATABASE_URL
  echo $EMAIL_HOST_USER
  ```
  
- [ ] **Database Configured**
  ```bash
  # Test connection
  python manage.py dbshell
  
  # Run migrations
  python manage.py migrate
  ```

- [ ] **Static Files Collected**
  ```bash
  python manage.py collectstatic --noinput
  ```

- [ ] **Debug is Disabled**
  ```bash
  # Verify in settings
  grep "^DEBUG" .env
  # Should output: DEBUG=False
  ```

- [ ] **ALLOWED_HOSTS Set Correctly**
  ```bash
  # For Railway
  ALLOWED_HOSTS=your-app.railway.app,www.your-app.railway.app
  
  # For Render
  ALLOWED_HOSTS=your-app.onrender.com
  ```

- [ ] **SSL/HTTPS Enabled**
  ```bash
  # Railway/Render auto-provides HTTPS
  # VPS: Use Let's Encrypt certbot
  ```

- [ ] **Email Configuration Tested**
  ```python
  python manage.py shell
  >>> from django.core.mail import send_mail
  >>> send_mail('Test', 'This is a test', 'from@gmail.com', ['to@example.com'])
  ```

- [ ] **Superuser Created**
  ```bash
  python manage.py createsuperuser
  ```

- [ ] **Admin Panel Working**
  ```
  Visit: https://your-domain/admin
  Login with superuser credentials
  ```

- [ ] **No Hardcoded Secrets**
  ```bash
  git log --all -S "password" -- "*.py"
  git log --all -S "secret" -- "*.py"
  # Should return no private keys/passwords
  ```

- [ ] **CORS/CSRF Configured**
  ```bash
  CORS_ALLOWED_ORIGINS=https://your-domain.com
  CSRF_TRUSTED_ORIGINS=https://your-domain.com
  ```

- [ ] **Backup Strategy**
  - [ ] Database backups scheduled
  - [ ] Media files backed up
  - [ ] Code repository backed up

- [ ] **Monitoring Setup**
  ```bash
  # Optional but recommended
  SENTRY_DSN=https://your-key@sentry.io/project
  ```

- [ ] **Performance Test**
  ```bash
  # Simple load test
  ab -n 100 -c 10 https://your-domain/
  ```

---

## 🔧 Troubleshooting

### Issue: Database Connection Failed

```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:password@host:port/dbname

# Test connection
python manage.py dbshell

# For Railway, check connected services
railway services
```

### Issue: Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# In settings, verify:
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

### Issue: OutOfMemory Error in Docker

```bash
# Check resource limits
docker stats obdms_web

# Increase Docker memory in docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
```

### Issue: Emails Not Sending

```bash
# Verify credentials
python manage.py shell
>>> import os
>>> print(f"Email: {os.environ.get('EMAIL_HOST_USER')}")

# Test Gmail App Password generation
# https://myaccount.google.com/apppasswords
```

### Issue: Railway Deployment Fails

```bash
# Check logs
railway logs

# Verify environment variables
railway variables

# Redeploy
railway deploy
```

### Debug Mode (Development Only)

```bash
# Enable for troubleshooting
DEBUG=True python manage.py runserver

# Don't forget to disable before production!
```

---

## 🔐 Security

### Production Security Checklist

- [x] **DEBUG = False** - Never enable in production
- [x] **SECRET_KEY Changed** - Generate new one for production
- [x] **HTTPS/SSL** - Railway/Render provide free SSL
- [x] **ALLOWED_HOSTS Set** - Prevent Host Header attacks
- [x] **CSRF Protection** - Django middleware enabled
- [x] **XSS Protection** - Security headers configured
- [x] **SQL Injection** - Using Django ORM (safe)
- [x] **Secrets in .env** - Never commit credentials
- [x] **CORS Configured** - Restrict origins
- [x] **Password Validation** - 8+ chars, complexity rules
- [x] **Session Security** - HTTPS-only, HttpOnly cookies
- [x] **Database Encryption** - PostgreSQL supports SSL

### Generate New SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Environment Variables Security

```bash
# ✅ GOOD - Use .env file
DATABASE_URL=postgresql://...

# ❌ BAD - Don't commit .env
git add .env  # Never do this!

# ✅ GOOD - Commit only .env.example
git add .env.example
```

### SSL/TLS Settings (Already Configured)

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

---

## 📞 Support & Resources

- **Django Docs**: https://docs.djangoproject.com
- **Railway Docs**: https://docs.railway.app/deploy/django
- **Render Docs**: https://render.com/docs/deploy-django
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

## 📝 Deployment Summary

| Platform | Cost | Setup Time | Difficulty | Recommendation |
|----------|------|-----------|-----------|-----------------|
| Railway | Free-$20 | 5 min | ⭐ Easy | ✅ **BEST** |
| Render | Free-$12 | 10 min | ⭐ Easy | ✅ Good |
| Fly.io | Free-$10 | 15 min | ⭐⭐ Medium | ✅ Good |
| AWS EC2 | $5-50 | 60 min | ⭐⭐⭐ Hard | Alternative |
| DigitalOcean | $5-20 | 30 min | ⭐⭐ Medium | Alternative |

---

## 🎯 Next Steps

1. **Choose Deployment Platform** → Railway (recommended)
2. **Set Up Environment** → Copy .env.example → .env
3. **Configure Database** → PostgreSQL (not SQLite)
4. **Configure Email** → Gmail App Password
5. **Deploy** → One-click from GitHub
6. **Monitor** → Check Railway dashboard
7. **Go Live** → Update DNS records

---

**Last Updated**: March 2026
**Status**: ✅ Production Ready
**Version**: 1.0.0
