from core.redis_sync import redis_client
import json

def publish_notification(user_id, title, description):
    payload = {
        "user_id": user_id,
        "title": title,
        "description": description,
    }
    redis_client.publish("notification", json.dumps(payload))
