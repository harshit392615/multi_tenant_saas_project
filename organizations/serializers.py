from rest_framework import serializers
from .models import Organization

class Organization_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id','name','created_at','slug','type']
