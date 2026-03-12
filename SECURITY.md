# Security Best Practices for OBDMS

## 🔐 Authentication & Authorization

### Password Policy
- ✅ Minimum 8 characters (configured in settings)
- ✅ Not similar to username/email
- ✅ Cannot be common password
- ✅ Cannot be only numeric

### Session Management
```python
# ✅ Configured in settings
SESSION_COOKIE_SECURE = True        # HTTPS only
SESSION_COOKIE_HTTPONLY = True      # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'     # CSRF protection
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Database sessions
```

### User Access Control
- ✅ Login required decorator on sensitive views
- ✅ Permission checks for admin actions
- ✅ Time-based session expiration (2 weeks)

---

## 🔒 Data Protection

### Encryption at Rest
- [ ] Database encryption (PostgreSQL with pgcrypto)
- [ ] Media files encryption (optional, for sensitive data)
- [ ] Backup encryption

### Encryption in Transit
- ✅ HTTPS enforced (SECURE_SSL_REDIRECT = True)
- ✅ HSTS headers configured
- ✅ TLS 1.2+ required
- ✅ Strong ciphers configured

### Sensitive Data Handling
```python
# ✅ Email credentials in environment variables
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# ✅ Database credentials in DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")

# ✅ Secret key never hardcoded
SECRET_KEY = os.environ.get("SECRET_KEY")
```

---

## 🛡️ Web Application Security

### CORS & CSRF
```python
# ✅ CORS restricted to specific origins
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

# ✅ CSRF tokens on all forms
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# ✅ Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'"),
    "style-src": ("'self'", "'unsafe-inline'"),
}
```

### Security Headers
```python
# ✅ Frame deny (prevent clickjacking)
X_FRAME_OPTIONS = "DENY"

# ✅ XSS protection
SECURE_BROWSER_XSS_FILTER = True

# ✅ HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Middleware Stack
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ... other middleware ...
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

## 🔑 Secret Management

### Environment Variables
```bash
# ✅ Never commit secrets
# .gitignore includes
.env
.env.local

# ✅ Only commit template
git add .env.example
git add requirements.txt

# ✅ Verify before pushing
git diff --cached | grep -i "password\|secret\|key"  # Should be empty
```

### Secret Detection
```bash
# Run before commits
trufflesecurity filesystem .
pip install detect-secrets
detect-secrets scan
```

### Rotation Policy
- [ ] SECRET_KEY rotated quarterly
- [ ] Database passwords rotated quarterly
- [ ] Email credentials rotated if changed
- [ ] API keys rotated immediately if leaked

---

## 🚨 Error Handling & Logging

### Secure Logging
```python
# ✅ Don't log sensitive data
# ❌ BAD
logger.info(f"User login: {username}, password: {password}")

# ✅ GOOD
logger.info(f"User login attempted: {username}")

# ✅ Configured in settings
LOGGING = {
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/django.log",
        },
    },
}
```

### Error Tracking
- ✅ Sentry configured for production errors
- ✅ 404/500 errors monitored
- ✅ No sensitive data in error messages
- ✅ Stack traces not shown to users

### Debug Mode
```python
# ✅ MUST be False in production
DEBUG = False

# ✅ Verify before deploying
if DEBUG:
    raise ValueError("DEBUG cannot be True in production!")
```

---

## 🗄️ Database Security

### Connection Security
```python
# PostgreSQL with SSL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "obdms_db",
        # Connection options
        "OPTIONS": {
            "sslmode": "require",
            "connect_timeout": 10,
        }
    }
}
```

### SQL Injection Prevention
- ✅ Using Django ORM (parameterized queries)
- ✅ Never use string formatting for queries
- ✅ User input always escaped

```python
# ✅ SAFE - Using ORM
BloodRequest.objects.filter(blood_group=user_input)

# ❌ UNSAFE - Never do this
BloodRequest.objects.raw(f"SELECT * FROM blood_requests WHERE blood_group = '{user_input}'")
```

### Database Access Control
- [ ] Least privilege principle (use specific DB user for app)
- [ ] No admin credentials in code
- [ ] Connection whitelist configured
- [ ] Backup credentials secured

---

## 🔍 Input Validation

### Form Validation
```python
# ✅ Django forms validate input
class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['phone', 'email', 'blood_group']
        # Django auto-validates data types and formats
```

### Length Limits
```python
# ✅ Set maximum lengths
email = models.EmailField(max_length=254)
phone = models.CharField(max_length=20)
```

### File Upload Security
```python
# ✅ Validate file type and size
# In views:
if file.size > 5 * 1024 * 1024:  # 5MB limit
    raise ValueError("File too large")

acceptable_types = ['image/jpeg', 'image/png']
if file.content_type not in acceptable_types:
    raise ValueError("Invalid file type")
```

---

## 🔐 Third-Party Security

### Gmail SMTP Security
- ✅ Use App Password (not main account password)
- ✅ Enable 2FA on Gmail account
- ✅ App password rotated quarterly
- ✅ Never log password in code/logs

### Dependency Management
```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies regularly
pip install --upgrade -r requirements.txt

# Lock version numbers
pip freeze > requirements-locked.txt
```

---

## 🚀 Deployment Security

### Secrets in CI/CD
```yaml
# ✅ GitHub Actions - use secrets
env:
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

# ❌ Never commit secrets
secrets:
  SECRET_KEY: my-actual-secret-key  # BAD!
```

### Container Security
```dockerfile
# ✅ Run as non-root user
USER django

# ✅ Use slim base image
FROM python:3.11-slim

# ✅ Don't run as root in production
# RUN useradd -m django
```

---

## 📊 Security Checklist

### Before Production Deployment
- [ ] DEBUG = False
- [ ] SECRET_KEY changed from default
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled and certificate valid
- [ ] Database backup strategy in place
- [ ] Logging configured (no sensitive data)
- [ ] Error tracking (Sentry) enabled
- [ ] Static files served securely
- [ ] No hardcoded credentials in code
- [ ] Dependencies scanned for vulnerabilities
- [ ] .env file not committed
- [ ] Security headers configured
- [ ] Session timeout configured
- [ ] CORS properly restricted
- [ ] CSRF protection enabled
- [ ] SSL certificate renewal automated

### Regular Security Audits
- [ ] Monthly: Review access logs for anomalies
- [ ] Quarterly: Security dependency updates
- [ ] Quarterly: Penetration testing
- [ ] Semi-annually: Full security audit
- [ ] Annually: Disaster recovery drill

---

## 🆘 Incident Response

### If Secrets Are Leaked
1. [ ] Immediately rotate all secrets
2. [ ] Change SECRET_KEY
3. [ ] Reset database passwords
4. [ ] Reset API keys
5. [ ] Review who had access
6. [ ] Update .env in all deployments
7. [ ] Monitor for unauthorized access
8. [ ] Create incident report

### If Security Breach Detected
1. [ ] Stop the application
2. [ ] Notification to stakeholders
3. [ ] Activate incident response team
4. [ ] Preserve logs for investigation
5. [ ] Notify affected users
6. [ ] Patch vulnerability
7. [ ] Deploy fix and monitor
8. [ ] Post-mortem analysis

---

## 🔗 Security Resources

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Django Security**: https://docs.djangoproject.com/en/stable/topics/security/
- **PostgreSQL Security**: https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-STRINGS
- **NIST Cybersecurity**: https://www.nist.gov/cyberframework

---

## 👥 Security Contacts

- Security Lead: [Name] - [Email]
- DevOps: [Name] - [Email]
- On-call: [Phone]

---

*Last Updated: March 2026*
*Version: 1.0.0*
