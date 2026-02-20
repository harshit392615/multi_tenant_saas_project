import redis.asyncio as redis
from django.conf import settings
redis_client = redis.from_url(settings.REDIS_LOCATION)