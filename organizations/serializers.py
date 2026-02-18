from rest_framework import serializers
from .models import Organization , Membership , Subscription

class Organization_Create_Serializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(
        choices = ['personal','team']
    )

class Organization_Serializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    slug = serializers.CharField()
    type = serializers.ChoiceField(
        choices = ['personal','team']
    )

class Organization_Update_Serializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.CharField()

class Organization_Archive_Serializer(serializers.Serializer):
    slug = serializers.CharField()

class Membership_add_update(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices = [
        "admin",'member','viewer'
        ]
    )

class Membership_Get(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.ChoiceField(
        choices = [
        "owner","admin",'member','viewer'
        ]
    )
    email = serializers.EmailField()
    status = serializers.IntegerField()