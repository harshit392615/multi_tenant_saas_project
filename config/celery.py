import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

broker_url = settings.CELERY_BROKER_URL
backend_url = settings.CELERY_RESULT_BACKEND

app.conf.broker_url = broker_url
app.conf.result_backend = backend_url

if (broker_url and broker_url.startswith("rediss://")) or \
   (backend_url and backend_url.startswith("rediss://")):
    ssl_options = {"ssl_cert_reqs": "CERT_NONE"}  # Use CERT_REQUIRED for production
    app.conf.broker_transport_options = ssl_options
    app.conf.redis_backend_use_ssl = ssl_options