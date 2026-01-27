from rest_framework import serializers
from .models import BaseNotification

class Notification_serializer(serializers.ModelSerializer):
    class Meta:
        model = BaseNotification
        fields = ['title','description']