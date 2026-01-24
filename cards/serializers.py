from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'title','description','status','due_date','assignee','created_at','slug'
        )
class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'title','description','status','due_date',
        )