from rest_framework.views import APIView
from organizations.views import TenantAPIviews
from rest_framework.response import Response
from .serializers import Invitation_Serializer , Accept_Serializer
from .services import invite_user , accept_invite
from rest_framework import status
from django.db import transaction
from .tasks import send_invitation_email
from django.utils import timezone

# Create your views here.

class Invite_User_API(TenantAPIviews):
    def post(self , request):
        with transaction.atomic():
            serializer = Invitation_Serializer(data = request.data)
            print(serializer)
            serializer.is_valid(raise_exception=True)

            invitation = invite_user(
                organization=request.organization,
                actor=request.membership,
                expires_at = timezone.now() + timezone.timedelta(days=7),
                **serializer.validated_data,
            )
            
            transaction.on_commit(
                lambda: send_invitation_email.delay(
                    email = invitation.email,
                    org_name = invitation.organization.name,
                    token = str(invitation.token),
                )
            )
            return Response({"message": "Invitation sent successfully"},status=status.HTTP_200_OK)
    
class Accept_User_API(TenantAPIviews):
    def post(self , request):
        serializer = Accept_Serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        accept_invite(token = serializer.validated_data['token'] , user=request.user)

        return Response({"message":"Invitation accepted successfully"},status=status.HTTP_200_OK)