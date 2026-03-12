# Static Files Deployment Guide - OBDMS

## ✅ Fixed Configuration Summary

### 1. **Development Settings (obdms/settings.py)** - ✅ FIXED
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ← Added
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Static Files Configuration
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # ← Added

# Media Files Configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### 2. **URL Configuration (obdms/urls.py)** - ✅ FIXED
```python
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your paths ...
]

# Serve static and media files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: WhiteNoise handles static, but media still needs serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. **Requirements (requirements.txt)** - ✅ ALREADY CORRECT
```
whitenoise==6.6.0  # Already included
```

### 4. **Templates (templates/base.html)** - ✅ CORRECT
```html
{% load static %}  <!-- ✅ Present at top -->
<link rel="stylesheet" href="{% static 'style.css' %}">  <!-- ✅ Using template tag -->
```

### 5. **.gitignore** - ✅ FIXED
Removed `/staticfiles/` and `/media/` ignore entries to allow deployment.

---

## 🚀 Pre-Deployment Steps (Run These Before Deploying)

### **Local Testing First**
```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run collectstatic to gather all static files
python manage.py collectstatic --noinput

# 3. Run in DEBUG=False mode to test production behavior locally
# Create/Edit .env file
echo DEBUG=False >> .env
echo STATIC_ROOT=staticfiles >> .env

# 4. Test local server
python manage.py runserver

# 5. Verify CSS loads at: http://localhost:8000/
# Check browser DevTools > Network tab, look for style.css with 200 status
```

---

## 📋 Deployment Checklist for Render/Wasmer

### **Step 1: Clear Old Static Files**
```bash
# Remove old collected static files
Remove-Item -Path "staticfiles" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "media" -Recurse -Force -ErrorAction SilentlyContinue
```

### **Step 2: Collect Static Files**
```bash
python manage.py collectstatic --noinput --verbosity=2
```

### **Step 3: Verify Collected Files**
```bash
# Check staticfiles directory exists and contains files
Get-ChildItem -Path "staticfiles" -Recurse | Measure-Object
```

### **Step 4: Git Commit and Push**
```bash
# Stage all changes including static files
git add -A

# Commit
git commit -m "Fix: Configure static files with WhiteNoise for production"

# Push to remote
git push origin main
```

---

## ⚙️ Render Deployment Configuration

### **In Render Dashboard:**

1. **Build Command** (in render.yaml or Dashboard):
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

2. **Start Command**:
   ```bash
   gunicorn obdms.wsgi:application
   ```

3. **Environment Variables** (Set in Render Dashboard):
   ```
   DEBUG=False
   SECRET_KEY=<your-secret-key>
   ALLOWED_HOSTS=yourdomain.render.com,www.yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.render.com
   DATABASE_URL=<your-postgres-url>
   ```

4. **Static Files Serving**:
   - ✅ WhiteNoise handles `/static/*` automatically
   - ✅ Both `style.css` and images will be served

---

## 🔍 Testing After Deployment

### **1. View Page Source**
- Open deployed site in browser
- Right-click → View Page Source
- Look for: `<link rel="stylesheet" href="/static/style.css?<hash>>`
- If you see this with the hash, WhiteNoise is working!

### **2. Check Network Tab (DevTools)**
- Open DevTools → Network tab
- Reload page
- Find `style.css` in the list
- Status should be **200** (not 404)
- Size should be correct (e.g., 23.0 KB)

### **3. Check Rendered Page**
- CSS should be applied (styled navbar, colors, layout)
- Images should be visible
- Bootstrap icons should show

---

## ❌ If CSS Still Doesn't Load

### **Troubleshooting:**

1. **Check Render Logs**:
   ```bash
   # View Render build logs
   # Look for: "collectstatic --noinput" completion message
   # Check for errors like: "FileNotFoundError"
   ```

2. **Verify Static Files Exist**:
   ```bash
   # SSH into Render instance (if available)
   ls -la /opt/render/project/src/staticfiles/
   ```

3. **Check CSS Path**:
   - Ensure `/staticfiles/style.css` actually exists
   - File permissions should allow reading

4. **Browser Cache**:
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Clear browser cache
   - Try in incognito mode

5. **Check WhiteNoise Middleware**:
   - Verify it's in MIDDLEWARE right after SecurityMiddleware
   - Verify `STATICFILES_STORAGE` config is set

---

## 📝 Common Issues After Deployment

| Issue | Cause | Solution |
|-------|-------|----------|
| CSS/images missing | Static files not collected | Run `collectstatic --noinput` in build command |
| 404 errors for static | Wrong STATIC_URL or STATIC_ROOT | Check settings.py paths |
| Broken image links | Using hardcoded `/static/` paths | Use `{% static 'file.css' %}` tag in templates |
| WhiteNoise not compressing | STATICFILES_STORAGE not set | Add `CompressedManifestStaticFilesStorage` |
| Files ignored by git | `/staticfiles/` still in .gitignore | Remove that line from .gitignore |

---

## 📦 Final File Structure

After `collectstatic`, your directory should look like:

```
project-root/
├── static/                    # Source static files
│   └── style.css
├── staticfiles/               # ✨ Collected static files (NEW)
│   ├── style.css
│   └── style.css.gz          # Compressed by WhiteNoise
├── media/                     # Uploaded media files (if any)
├── obdms/
│   ├── settings.py           # ✅ Updated
│   ├── settings_production.py
│   ├── urls.py               # ✅ Updated
│   └── wsgi.py
├── manage.py
├── requirements.txt          # ✅ Has whitenoise
├── .gitignore               # ✅ Fixed
└── .env                     # DEBUG=False, etc.
```

---

## 🎯 Next Steps

1. ✅ Run `collectstatic` locally
2. ✅ Test with `DEBUG=False` locally
3. ✅ Commit all changes to git
4. ✅ Push to Render
5. ✅ Verify CSS loads in browser
6. ✅ Check browser DevTools Network tab
7. ✅ Monitor Render logs for any issues

---

## 📚 References

- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Django Static Files Guide](https://docs.djangoproject.com/en/5.0/howto/static-files/)
- [Render Deployment Guide](https://render.com/docs/deploy-flask)

