web: gunicorn obdms.wsgi --log-file - --log-level info --workers 4 --bind 0.0.0.0:$PORT --timeout 60
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
