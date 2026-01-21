from rest_framework import serializers
from .models import Workspace

class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id","name"]

class WorkspaceOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id","name",'slug']