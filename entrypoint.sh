#!/bin/bash
set -e

echo "Starting OBDMS Django Application..."

# Create necessary directories
mkdir -p logs media staticfiles

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (production setup)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print("Superuser created successfully")
else:
    print("Superuser already exists")
END
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    obdms.wsgi:application
