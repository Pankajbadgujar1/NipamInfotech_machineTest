from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import (
    ClientSerializer, ClientDetailSerializer, 
    ProjectSerializer, ProjectCreateSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Client model providing CRUD operations.
    
    list: Get all clients
    create: Create a new client
    retrieve: Get a specific client with its projects
    update: Update a client
    destroy: Delete a client
    """
    queryset = Client.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='projects')
    def create_project(self, request, pk=None):
        """
        Create a new project for a specific client.
        
        Args:
            request: HTTP request containing project details
            pk: Primary key of the client
            
        Returns:
            Response with the created project data
        """
        client = self.get_object()
        serializer = ProjectCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            users = serializer.validated_data.pop('users')
            project = serializer.save(
                client=client,
                created_by=request.user
            )
            project.users.set(users)
            
            # Return full project data
            response_serializer = ProjectSerializer(project)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Project model providing read operations for the logged-in user.
    
    list: Get all projects assigned to the logged-in user
    """
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        """
        Return only projects assigned to the logged-in user.
        """
        return Project.objects.filter(users=self.request.user)