class JWTAuthenticationMiddleware:
    def __init__(self,inner):
        self.inner = inner

    async def __call__(self, scope, receive , send):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from django.contrib.auth.models import AnonymousUser
        from channels.db import database_sync_to_async
        from urllib.parse import parse_qs

        auth = JWTAuthentication()

        query_string = scope["query_string"].decode()
       
        query = parse_qs(query_string)
        token = query.get("token" , [None])[0]
        note_id = query.get("note_id" , [None])[0]

        scope['note_id'] = note_id

        if token:
            try:
                validated_token = auth.get_validated_token(token)
                user = await database_sync_to_async(auth.get_user)(validated_token)
                scope['user'] = user
            except Exception:
                scope['user'] = AnonymousUser()
            
        
        return await self.inner(scope , receive , send)
    
class OrganizationMiddleware:
    def __init__(self,inner):
        self.inner = inner
    
    def check_user_permissions(self , user , note_id):
        from organizations.models import Membership
        from notes.models import Notes
        organization = Notes.objects.get(id = note_id).organization
        membership_status = Membership.objects.filter(user = user , organization = organization).exists()

        return membership_status
    
    async def __call__(self, scope, receive , send):
        from asgiref.sync import sync_to_async
       
        note_id = scope['note_id']

        user = scope['user']

        scope['membership'] = await sync_to_async(self.check_user_permissions)(user , note_id)

        print(scope['membership'])

        return await self.inner(scope , receive , send)
    