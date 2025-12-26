from rest_framework import serializers
from .models import User

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 200 )
    email = serializers.EmailField()
    password = serializers.CharField(min_length = 8 , write_only = True)

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user