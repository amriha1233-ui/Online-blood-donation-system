#!/usr/bin/env python
"""
Security audit script - checks for common security issues
Run before deployment: python security_audit.py
"""

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{CYAN}{text.center(60)}{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

# Security checks
issues = []
warnings = []

print_header("SECURITY AUDIT")

# Check 1: DEBUG setting
print("Checking DEBUG setting...")
settings_file = BASE_DIR / "obdms" / "settings.py"
if settings_file.exists():
    content = settings_file.read_text()
    if 'DEBUG = True' in content and 'os.environ.get("DEBUG"' not in content:
        print_error("DEBUG is hardcoded to True")
        issues.append("DEBUG hardcoded")
    else:
        print_success("DEBUG is controlled via environment variable")
else:
    print_warning("Could not find settings.py")

# Check 2: Secret key
print("\nChecking SECRET_KEY...")
env_file = BASE_DIR / ".env"
if env_file.exists():
    print_success(".env file exists")
else:
    print_warning(".env file not found (create from .env.example)")

# Check 3: Look for hardcoded secrets
print("\nScanning for hardcoded secrets...")
patterns = {
    'AWS Key': r"AKIA[0-9A-Z]{16}",
    'Google API': r"AIza[0-9A-Za-z\-_]{35}",
    'Stripe Key': r"(sk_live|pk_live)_[A-Za-z0-9_]{20}",
    'Email Password': r"password\s*=\s*['\"]([^'\"]{8,})['\"]",
    'Database URL': r"postgresql://[^/]+:[^/]+@[^\s]+",
    'OAuth Token': r"oauth[_-]?token\s*=\s*['\"]?[A-Za-z0-9_]{20,}",
}

sensitive_files = list(BASE_DIR.rglob("*.py"))
sensitive_files = [f for f in sensitive_files if ".venv" not in str(f) and "migrations" not in str(f)]

found_secrets = False
for pattern_name, pattern in patterns.items():
    for file in sensitive_files[:50]:  # Check first 50 files
        try:
            content = file.read_text(errors='ignore')
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                if 'example' not in str(file) and 'test' not in str(file):
                    print_error(f"Possible {pattern_name} in {file}:{line_num}")
                    found_secrets = True
        except Exception:
            pass

if not found_secrets:
    print_success("No obvious hardcoded secrets found")

# Check 4: Requirements
print("\nChecking production packages...")
req_file = BASE_DIR / "requirements.txt"
if req_file.exists():
    content = req_file.read_text()
    required_packages = {
        'gunicorn': 'WSGI server',
        'psycopg2-binary': 'PostgreSQL support',
        'whitenoise': 'Static files',
        'django-redis': 'Caching',
        'dj-database-url': 'Database URL parsing',
    }
    
    for package, description in required_packages.items():
        if package in content:
            print_success(f"{package} ({description})")
        else:
            print_warning(f"Missing: {package} ({description})")
else:
    print_error("requirements.txt not found")

# Check 5: ALLOWED_HOSTS
print("\nChecking ALLOWED_HOSTS...")
if settings_file.exists():
    content = settings_file.read_text()
    if 'ALLOWED_HOSTS' in content and 'os.environ.get' in content:
        print_success("ALLOWED_HOSTS is environment-controlled")
    else:
        print_warning("ALLOWED_HOSTS may need to be updated")

# Check 6: CSRF and CORS
print("\nChecking CSRF/CORS settings...")
if settings_file.exists():
    content = settings_file.read_text()
    if 'CSRF_COOKIE_SECURE' in content:
        print_success("CSRF protection configured")
    else:
        print_warning("CSRF protection may need configuration")
    
    if 'CORS' in content:
        print_success("CORS configuration present")
    else:
        print_warning("CORS may need configuration")

# Check 7: SSL/TLS
print("\nChecking SSL/TLS settings...")
if settings_file.exists():
    content = settings_file.read_text()
    ssl_settings = [
        'SECURE_SSL_REDIRECT',
        'SESSION_COOKIE_SECURE',
        'SECURE_HSTS_SECONDS'
    ]
    for setting in ssl_settings:
        if setting in content:
            print_success(f"{setting} configured")
        else:
            print_warning(f"{setting} not found")

# Check 8: Database
print("\nChecking database configuration...")
if settings_file.exists():
    content = settings_file.read_text()
    if 'sqlite' in content.lower():
        print_warning("SQLite detected - not recommended for production")
    if 'postgresql' in content.lower() or 'dj_database_url' in content:
        print_success("PostgreSQL/environment-based DB configured")

# Check 9: Email
print("\nChecking email configuration...")
if settings_file.exists():
    content = settings_file.read_text()
    if 'EMAIL_HOST_USER' in content and 'os.environ' in content:
        print_success("Email configuration is environment-controlled")
    else:
        print_warning("Email configuration may need updating")

# Check 10: Logging
print("\nChecking logging configuration...")
if settings_file.exists():
    content = settings_file.read_text()
    if 'LOGGING' in content:
        print_success("Logging configuration present")
    else:
        print_warning("Logging not configured (recommended for production)")

# Summary
print_header("SECURITY AUDIT SUMMARY")
print(f"Total Issues: {len(issues)}")
print(f"Total Warnings: {len(warnings)}")

if issues:
    print(f"\n{RED}Critical Issues Found:{RESET}")
    for issue in issues:
        print_error(issue)

if warnings:
    print(f"\n{YELLOW}Warnings:{RESET}")
    for warning in warnings:
        print_warning(warning)

if not issues:
    print_success("No critical security issues found!")
    print("\nYour project is ready for production deployment.")

sys.exit(1 if issues else 0)
