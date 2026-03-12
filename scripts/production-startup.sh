#!/bin/bash
# Production startup script for Docker

set -e

echo "🚀 OBDMS Production Setup..."

# Create necessary directories
mkdir -p logs media staticfiles

# Wait for database to be ready
echo "Waiting for database connection..."
while ! python -c "import os; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obdms.settings'); django.setup(); from django.db import connection; connection.ensure_connection()" 2>/dev/null; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

echo "PostgreSQL is up - executing migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Production setup complete!"
