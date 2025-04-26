from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    """
    Client model to store client information
    """
    client_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clients')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name


class Project(models.Model):
    """
    Project model to store project information.
    """
    project_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')

    def __str__(self):
        return f"{self.project_name} - {self.client.client_name}"