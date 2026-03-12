# ⚡ QUICK START - DEPLOYMENT IN 5 MINUTES (Railway)

This guide will get your OBDMS app live in production by the end of today.

## Prerequisites (5 minutes)

### 1. Generate SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copy the output
```

### 2. Create Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. If needed, enable 2-factor authentication first
3. Select "Mail" and "Windows Computer"
4. Generate app password
5. Copy the 16-character password (spaces removed)

### 3. Have These Ready
- [ ] Your GitHub repository URL
- [ ] Generated SECRET_KEY (from step 1)
- [ ] Gmail address (EMAIL_HOST_USER)
- [ ] Gmail App Password (from step 2)
- [ ] Your desired domain or subdomain

---

## Deployment (5 minutes on Railway)

### Step 1: Sign Up (1 minute)
1. Go to https://railway.app
2. Click "Start for free"
3. Sign in with GitHub
4. Authorize Railway to access your repositories

### Step 2: Create Project (1 minute)
1. Dashboard → "Create New Project"
2. "Deploy from GitHub repo"
3. Select your repository
4. Select branch: `main` (or `production`)
5. Wait for auto-detection (should detect Django)

### Step 3: Configure Environment Variables (2 minutes)
After clicking "Deploy", you'll see the deployment panel:

```
Click on: Variables → Add Variable
```

Add all of these:

| Variable | Value | Example |
|----------|-------|---------|
| `DEBUG` | `False` | False |
| `SECRET_KEY` | *Your generated key* | abc123... |
| `ALLOWED_HOSTS` | your-app.railway.app | your-app.railway.app |
| `EMAIL_HOST_USER` | your-email@gmail.com | myemail@gmail.com |
| `EMAIL_HOST_PASSWORD` | your-app-password | xxxx xxxx xxxx xxxx |
| `ENVIRONMENT` | production | production |

**Note**: Railway automatically sets up PostgreSQL. No extra steps needed!

### Step 4: Deploy (1 minute)
1. In the deployment panel, click the "Build & Deploy" button
2. Watch the logs scroll by
3. Should complete in 30-90 seconds
4. Look for: `✓ Deployment successful`

### Step 5: Verify (1 minute)

Once deployed:

```bash
# View deployment URL in Railway dashboard
# Usually: https://yourapps-name.railway.app

# Test it works:
curl https://yourapps-name.railway.app/health/
# Should return: {"status": "healthy", ...}

# Access admin:
https://yourapps-name.railway.app/admin/
```

---

## What Happens Automatically

Railway automatically:
- ✅ Creates PostgreSQL database (DATABASE_URL set)
- ✅ Runs migrations (`python manage.py migrate`)
- ✅ Collects static files
- ✅ Sets up HTTPS/SSL certificate
- ✅ Configures DNS
- ✅ Starts Gunicorn WSGI server

No additional configuration needed!

---

## Your App is Live! 🎉

Now you need to:

### 1. Create SuperUser (Admin Account)
```bash
# In Railway dashboard, click the "Web" service
# Click the terminal/console icon
# Run:
python manage.py createsuperuser

# Answer the prompts:
# Email: your-email@example.com
# Password: strong-password-here
```

Then login at: `https://yourapps-name.railway.app/admin/`

### 2. Test the Application
```bash
https://yourapps-name.railway.app/
# Should show home page

# Try registering as a donor/hospital
# Try creating a blood request
# Check if emails send (check inbox)
```

### 3. Monitor in First 24 Hours
```bash
# In Railway dashboard:
# - Click "Web" service
# - Watch "Logs" tab
# - Should be clean (no red ERROR messages)
# - Database: Click "PostgreSQL" to see status
```

---

## Common First-Time Issues & Fixes

**Issue: "Build failed"**
- Check logs for error message
- Usually a package import issue
- Ask: Did all requirements.txt packages install?

**Issue: "502 Bad Gateway"**
- App might still be starting (wait 30 seconds)
- Check logs: Any database connection error?
- Verify DATABASE_URL is set

**Issue: "Admin page shows 500 error"**
- Migrations didn't run
- In Railway console, run: `python manage.py migrate --check`

**Issue: "Emails not sending"**
- Check if Gmail App Password is correct (no spaces)
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are set
- Try sending test email from admin panel

---

## Connect Custom Domain (Optional)

If you want your-domain.com instead of your-app.railway.app:

1. In Railway dashboard: Settings → Custom Domain
2. Add your domain (e.g., yourdomain.com)
3. Copy the CNAME record provided
4. Go to your domain registrar (GoDaddy, Namecheap, Route53)
5. Add CNAME record: Railway's value
6. Wait 5-10 minutes for DNS propagation
7. Your-domain.com should work!

---

## Backup Your Database

Railway automatically backs up PostgreSQL, but you should also:

```bash
# Manual backup (if you have psql installed):
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql

# Or download from Railway dashboard:
# PostgreSQL → Data → Backups
```

---

## Need Help?

### Check These in Order:
1. **Read errors carefully** - Usually tells you exactly what's wrong
2. **Check logs** - Railway dashboard → Web → Logs tab
3. **Review documentation** - See README.md in your repo
4. **Run security audit** - `python security_audit.py`
5. **Check platforms docs** - https://docs.railway.app/deploy/django

### Common Commands:
```bash
# View production logs
railway logs -f

# Run command in production
railway run python manage.py shell

# List environment variables
railway variables

# Stop/restart application
# (Usually done via Railway dashboard)
```

---

## Success! 🚀

You should now have:

✅ OBDMS running on production  
✅ PostgreSQL database connected  
✅ Email notifications working  
✅ SSL/HTTPS automatically configured  
✅ Admin panel accessible  
✅ All static files serving correctly  
✅ Backups configured  

**Celebrate! You deployed your first Django app to production! 🎊**

---

## Next Steps (This Week)

- [ ] Test all user flows (register, create requests, get matched)
- [ ] Share with your team
- [ ] Monitor for any issues
- [ ] If everything works 24+ hours, tell others!
- [ ] Consider setting up error tracking (Sentry - optional)
- [ ] Plan any post-launch improvements

---

## Alternative Platforms (If You Want to Switch Later)

All these work similarly:

**Render** (https://render.com):
- Similar to Railway
- Free tier available
- GitHub auto-deploy

**Fly.io** (https://fly.io):
- Good for global deployment
- CLI-based (`flyctl deploy`)
- More control

**Your Own VPS**:
- Full control
- More manual setup
- See full deployment guide in README.md

---

## You Did It! 🎉

Your application is now in production serving real users.

Questions? Check README.md or SECURITY.md in your repository.

Welcome to the world of deployed applications! 🚀
