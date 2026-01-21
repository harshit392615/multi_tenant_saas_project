from rest_framework import serializers
from .models import Notes

class notes_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title','content']