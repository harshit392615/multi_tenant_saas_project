from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id',
            'organization',
            'actor',
            'action',
            'entity_type',
            'entity_id',
            'metadata',
            'created_at'
        )