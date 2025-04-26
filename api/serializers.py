from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Used for displaying basic user information.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal User serializer with only id and name.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name']

    def get_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.username


class ProjectMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal Project serializer for listing in client detail view.
    """
    class Meta:
        model = Project
        fields = ['id', 'project_name']


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for Client model for list and create operations.
    """
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


class ClientDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Client model with detailed information including projects.
    """
    created_by = serializers.ReadOnlyField(source='created_by.username')
    projects = ProjectMinimalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model for creating and listing projects.
    """
    client = serializers.ReadOnlyField(source='client.client_name')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    users = UserMinimalSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new project with user assignment.
    """
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    
    class Meta:
        model = Project
        fields = ['project_name', 'users']