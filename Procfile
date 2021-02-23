release: python manage.py migrate
web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker

