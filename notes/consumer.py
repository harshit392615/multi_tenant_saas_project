from channels.generic.websocket import AsyncWebsocketConsumer
import json
class NotesUpdateConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        from core.redis_async import redis_client
        from .selectors import get_note
        from asgiref.sync import sync_to_async

        self.note_id = self.scope["note_id"]
        self.group_name = f"note_{self.note_id}"

        if self.scope["user"].is_anonymous or not self.scope["membership"]:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Initialize doc_version if missing
        if not await redis_client.exists(f"doc_version:{self.note_id}"):
            await redis_client.set(f"doc_version:{self.note_id}", 0)

            content = await sync_to_async(get_note)(
                self.note_id, self.scope["membership"]
            )

            if content:
                version = await redis_client.incr(f"doc_version:{self.note_id}")
                await redis_client.xadd(
                    f"content:{self.note_id}:ops",
                    {
                        "type": "insert",
                        "pos": 0,
                        "content": content,
                        "version": version,
                    },
                )

        ops = await redis_client.xrange(f"content:{self.note_id}:ops")
        history = [op for _, op in ops]

        await self.send(text_data=json.dumps({
            "type": "init",
            "ops": history,
            "doc_version": int(await redis_client.get(f"doc_version:{self.note_id}")),
        }))

    # ---------------- OT TRANSFORM ---------------- #

    @staticmethod
    def transform(incoming, applied):
        print(type(applied["pos"]) , type(incoming["pos"]))
        incoming_pos = int(incoming["pos"])
        applied_pos = int(applied["pos"])
        if incoming["type"] == "insert" and applied["type"] == "insert":
            if applied_pos <= incoming_pos:
                incoming_pos += len(applied["content"])

        elif incoming["type"] == "insert" and applied["type"] == "delete":
            if applied_pos < incoming_pos:
                incoming_pos -= min(
                    applied["length"], incoming_pos - applied_pos
                )

        elif incoming["type"] == "delete" and applied["type"] == "insert":
            if applied_pos <= incoming_pos:
                incoming_pos += len(applied["content"])
            elif applied_pos < incoming_pos + incoming["length"]:
                incoming["length"] += len(applied["content"])

        elif incoming["type"] == "delete" and applied["type"] == "delete":
            i_start = incoming_pos
            i_end = incoming_pos + int(incoming["length"])
            a_start = applied_pos
            a_end = applied_pos + int(applied["length"])

            if a_end <= i_start:
                incoming_pos -= int(applied["length"])
            elif a_start >= i_end:
                pass
            else:
                overlap = min(i_end, a_end) - max(i_start, a_start)
                incoming["length"] -= overlap
                if a_start < i_start:
                    incoming_pos = a_start

        return incoming

    # ---------------- RECEIVE ---------------- #

    async def receive(self, text_data=None):
        from core.redis_async import redis_client

        data = json.loads(text_data)
        base_version = int(data["base_version"])
        print(data)

        # Fetch ops AFTER base_version
        ops = await redis_client.xrange(f"content:{self.note_id}:ops")
        history = [
            op for _, op in ops if int(op["version"]) > base_version
        ]

        # Transform incoming op
        incoming = data
        for applied in history:
            incoming = self.transform(incoming, applied)

        # Assign authoritative version
        new_version = await redis_client.incr(f"doc_version:{self.note_id}")
        incoming["version"] = new_version

        # Persist
        await redis_client.xadd(
            f"content:{self.note_id}:ops",
            incoming,
        )

        # Broadcast
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "sender",
                "message": json.dumps(incoming),
                "sender_channel":self.channel_name,
            },
        )

    async def sender(self, event):
        print(event)
        if event['sender_channel'] == self.channel_name:
            return
        await self.send(text_data=event["message"])

    # ---------------- DISCONNECT ---------------- #

    async def disconnect(self, close_code):
        from core.redis_async import redis_client
        from asgiref.sync import sync_to_async
        from .services import update_note

        await redis_client.srem(
            f"note:{self.note_id}:users",
            self.scope["user"].email,
        )

        count = await redis_client.scard(f"note:{self.note_id}:users")

        if count == 0:
            ops = await redis_client.xrange(f"content:{self.note_id}:ops")
            ordered_ops = sorted(
                [op for _, op in ops], key=lambda o: int(o["version"])
            )

            await sync_to_async(update_note)(self.note_id, ordered_ops)

            await redis_client.delete(f"content:{self.note_id}:ops")
            await redis_client.delete(f"doc_version:{self.note_id}")
