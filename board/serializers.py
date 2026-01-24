from rest_framework import serializers
from .models import Board

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','name']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','name','created_at','slug']