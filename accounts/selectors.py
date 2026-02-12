from core.redis_async import redis_client
import asyncio

async def get_status(user):
    try:
        while True:
            await redis_client.set(
                f"user:online:{user.id}",
                1,
                ex = 45
            )
            yield f"event: heartbeat\n data: {1}\n\n"
            await asyncio.sleep(20)

    except asyncio.CancelledError:
        pass