#!/bin/bash
# Local development setup script

set -e

echo "🔧 Setting up OBDMS development environment..."

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your local configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser (optional)..."
python manage.py createsuperuser --no-input 2>/dev/null || python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Development setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo "4. Admin: http://localhost:8000/admin"
