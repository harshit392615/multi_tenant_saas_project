from .models import UserNotification
import json
import asyncio
from core.redis_async import redis_client

def get_unseen_notifications(user):
    return list(
        UserNotification.objects.filter(user=user, seen=False)
    )

async def notification_stream(notifications , user):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("notification")

    try:
        # 1️⃣ handshake
        yield "data: connected\n\n"

        # 2️⃣ send unseen notifications
        for n in notifications:
            payload = {
                "title": n.title,
                "description": n.description,
            }
            yield f"data: {json.dumps(payload)}\n\n"

        # 3️⃣ listen for live notifications
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if message:
                data = json.loads(message["data"])
                if data.get("user_id") == user.id:
                    yield f"data: {json.dumps(data)}\n\n"

            await asyncio.sleep(0)  # cooperative multitasking
    finally:
            await pubsub.unsubscribe("notification")
            await pubsub.close()


    