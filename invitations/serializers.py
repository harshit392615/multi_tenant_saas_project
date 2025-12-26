from rest_framework import serializers
from .models import Invitation

class Invitation_Serializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=[
            'admin','member','viewer'
        ]
    )

class Accept_Serializer(serializers.Serializer):
    token = serializers.UUIDField()