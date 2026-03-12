# Deployment Checklist for OBDMS

## 🚀 Pre-Deployment (48 hours before launch)

### Infrastructure
- [ ] Cloud account created (Railway/Render/Fly.io)
- [ ] Domain registered and configured
- [ ] DNS records prepared (if custom domain)
- [ ] CDN setup (optional, for better performance)

### Code Quality
- [ ] All tests passing: `pytest --cov`
- [ ] Linting clean: `flake8 .`
- [ ] Code formatted: `black --check .`
- [ ] Import sorting: `isort --check-only .`
- [ ] No debug code left
- [ ] No print statements in production code
- [ ] Git repository clean (all changes committed)

### Environment Configuration
- [ ] `.env.example` created with all variables documented
- [ ] `.env` file created from `.env.example`
- [ ] `SECRET_KEY` generated: 
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Database credentials set
- [ ] Email credentials prepared
- [ ] All environment variables verified

### Settings.py
- [ ] `DEBUG = False` set
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] Secret key environment variable set
- [ ] Database URL points to production database
- [ ] Static files configuration verified
- [ ] Media files configuration verified
- [ ] Logging configured for production

### Database
- [ ] PostgreSQL instance created and accessible
- [ ] Database backup tested
- [ ] Initial migrations ready to run:
  ```bash
  python manage.py migrate --plan
  ```
- [ ] Database credentials stored securely (not in code)

### Static Files
- [ ] Collect static files successful:
  ```bash
  python manage.py collectstatic --dry-run
  ```
- [ ] Static files storage configured (WhiteNoise or CDN)
- [ ] CSS/JS assets updated and tested
- [ ] Images optimized and tested

### Email Configuration
- [ ] Gmail App Password generated
- [ ] Email settings tested:
  ```bash
  python manage.py shell
  # from django.core.mail import send_mail
  # send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
  ```
- [ ] Email template tested and working

### Docker Setup (if using)
- [ ] Dockerfile builds successfully:
  ```bash
  docker build -t obdms:latest .
  ```
- [ ] Docker image tested locally
- [ ] `.dockerignore` optimized
- [ ] Base image security scanned

### Security Scanning
- [ ] Secret key scan passed:
  ```bash
  trufflesecurity filesystem .
  ```
- [ ] No hardcoded passwords/API keys
- [ ] Dependencies scanned for vulnerabilities:
  ```bash
  pip install safety
  safety check
  ```
- [ ] OWASP Top 10 review completed

### Monitoring & Logging
- [ ] Error tracking setup (Sentry):
  ```bash
  SENTRY_DSN configured
  ```
- [ ] Logging configured and tested
- [ ] Log rotation setup
- [ ] Uptime monitoring configured

---

## ⚙️ Deployment Day

### 1. Final Code Push (2 hours before)
```bash
# Final commit and tag
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin main --tags

# Verify no uncommitted changes
git status  # Should be clean
```

### 2. Database Backup
```bash
# Create backup before deployment
pg_dump -U user -h host dbname > backup_$(date +%Y%m%d_%H%M%S).sql

# For Railway:
railway run pg_dump > backup.sql
```

### 3. Verify Environment Variables
```bash
# For Railway:
railway variables

# For Render:
# Check in dashboard Environment section

# Verify all required vars are set:
echo "Checking critical environment variables..."
railway variables | grep -E "SECRET_KEY|DATABASE_URL|EMAIL_HOST_USER"
```

### 4. Deploy Application
```bash
# Railway deployment
railway up

# Or Render deployment
# Trigger from GitHub: git push origin main

# Or Fly.io deployment
flyctl deploy
```

### 5. Monitor Deployment
```bash
# Watch logs in real-time
railway logs -f

# Or Fly.io
flyctl logs

# Or Render
# Check in dashboard > Logs
```

### 6. Verify Deployment
- [ ] Application started successfully (no 502/503 errors)
- [ ] Admin panel accessible: `https://your-domain/admin`
- [ ] Home page loads: `https://your-domain/`
- [ ] Login works
- [ ] Dashboard accessible after login
- [ ] Email sending works (test from admin)
- [ ] Static files loading (CSS/images visible)
- [ ] No console errors in browser DevTools

### 7. Run Post-Deployment Tests
```bash
# Health check
curl https://your-domain/health/

# Admin login test
# Visit https://your-domain/admin and login

# Email test
python manage.py shell
# from django.core.mail import send_mail
# send_mail('Production Test', 'This deployment works!', 'from@gmail.com', ['your-email@example.com'])

# Database connectivity
python manage.py dbshell
# \q or exit
```

### 8. Check Application Logs
```bash
# Watch for errors
railway logs -f --start-time "30m ago"

# Check specifically for errors
railway logs -f | grep -i "error\|exception\|critical"
```

---

## ✅ Post-Deployment (First 24 hours)

### Monitoring
- [ ] Application CPU < 80%
- [ ] Memory usage stable
- [ ] Database queries performing well
- [ ] No 5XX errors in logs
- [ ] Error tracking (Sentry) shows no critical issues
- [ ] Response times < 500ms average

### Functionality
- [ ] All user authentication flows working
- [ ] Create blood request functionality working
- [ ] Donor registration working
- [ ] Hospital registration working
- [ ] Email notifications sending
- [ ] File uploads working (if applicable)
- [ ] Admin panel fully functional

### Performance
- [ ] Page load time acceptable (< 3 seconds)
- [ ] Static files cached properly
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Background tasks completing

### Analytics
- [ ] Monitor to track key metrics:
  - Active users
  - Request rate
  - Error rate
  - Response time
  - Database query time

### Backups Verification
- [ ] Automated database backups configured
- [ ] Restore test successful
- [ ] Backup retention policy set
- [ ] Documentation updated

### Documentation
- [ ] Deployment documented
- [ ] Runbook created for common issues
- [ ] Team trained on monitoring
- [ ] Incident response plan established

---

## 🚨 Rollback Plan (If Issues Occur)

### Quick Rollback
```bash
# For Railway
railway rollback

# For Fly.io
fly rollback

# For Render
# Go to dashboard > Deploy > Select Previous
```

### Database Rollback
```bash
# Restore from backup if migrations failed
psql -U user -h host dbname < backup_YYYYMMDD_HHMMSS.sql
```

### Manual Rollback
```bash
# Stop current deployment
railway stop

# Checkout previous version
git checkout previous-tag

# Redeploy
railway deploy
```

---

## 🔄 Weekly Post-Deployment

- [ ] Review error logs
- [ ] Check database size and performance
- [ ] Verify all email notifications are sending
- [ ] Test mobile responsiveness
- [ ] Monitor uptime metrics
- [ ] Review user feedback/issues
- [ ] Security audit of recent changes
- [ ] Database maintenance/optimization

---

## 🔒 Security Post-Deployment

- [ ] SSL certificate valid and renewed
- [ ] No sensitive data in logs
- [ ] User permissions correctly configured
- [ ] Session timeout working
- [ ] Password reset functionality tested
- [ ] Account lockout after failed attempts working
- [ ] API rate limiting functional (if applicable)

---

## Critical Contacts & Resources

### Deployment Team
- DevOps Lead: [Name] - [Phone]
- Backend Lead: [Name] - [Phone]
- On-call: [Phone]
- PagerDuty: [Link]

### Platform Documentation
- Railway: https://docs.railway.app/deploy/django
- Render: https://render.com/docs/deploy-django
- Django: https://docs.djangoproject.com/en/stable/

### Emergency Contacts
- PostgreSQL Support: [Based on hosting]
- Email Provider Support: [Gmail/SendGrid]
- Domain Registrar: [Based on registrar]

---

## Sign-Off

- [ ] Project Manager: _________________ Date: _______
- [ ] Tech Lead/DevOps: _________________ Date: _______
- [ ] QA Lead: _________________ Date: _______

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Deployment Duration**: _______________
**Issues Encountered**: _______________
**Resolution**: _______________

---

*Last Updated: March 2026*
*Version: 1.0.0*
