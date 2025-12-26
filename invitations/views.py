from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Invitation_Serializer , Accept_Serializer
from .services import invite_user , accept_invite
from rest_framework import status
from django.db import transaction
from .tasks import send_invitation_email

# Create your views here.

class Invite_User_API(APIView):
    def post(self , request):
        with transaction.atomic():
            serializer = Invitation_Serializer(data = request.data)
            serializer.is_valid(raise_exception=True)


            invitation = invite_user(
                organization=request.organization,
                actor=request.membership,
                **serializer.validated_data,
            )
            
            transaction.on_commit(
                lambda: send_invitation_email.delay(
                    email = invitation.email,
                    org_slug = invitation.organization.slug,
                    token = str(invitation.token),
                )
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
    
class Accept_User_API(APIView):
    def post(self , request):
        serializer = Invitation_Serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        accept_invite(serializer.validated_data['token'] , user=request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)