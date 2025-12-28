from rest_framework import serializers
from .models import Organization

class Organization_Create_Serializer(serializers.Serializer):
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    slug = serializers.CharField()
    type = serializers.ChoiceField(
        choices = ['personal','team']
    )

class Organization_Update_Serializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.CharField()

class Organization_Archive_Serializer(serializers.Serializer):
    slug = serializers.CharField()