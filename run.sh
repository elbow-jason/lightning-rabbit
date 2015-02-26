source env/bin/activate
celery -A fibs worker --loglevel=info & python run.py