from rest_framework import serializers
from .models import Organization , Membership

class Organization_Create_Serializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(
        choices = ['personal','team']
    )

class Organization_Serializer(serializers.Serializer):
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

class Membership_add_update(serializers.ModelSerializer):
    
    class Meta:
        model = Membership
        fields = ['user' , 'role']

class Membership_Get(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ['user','role']