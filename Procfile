web: gunicorn translatebot.wsgi
worker: celery -A translatebot worker -B --loglevel=INFO
release: python manage.py migrate
