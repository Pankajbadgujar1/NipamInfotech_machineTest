from django.contrib import admin
from .models import Client, Project

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Client model.
    """
    list_display = ('client_name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('client_name', 'created_by__username')
    readonly_fields = ('created_at', 'created_by', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new client
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project model.
    """
    list_display = ('project_name', 'client', 'created_by', 'created_at')
    list_filter = ('client',)
    search_fields = ('project_name', 'client__client_name', 'created_by__username')
    filter_horizontal = ('users',)
    readonly_fields = ('created_at', 'created_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new project
            obj.created_by = request.user
        super().save_model(request, obj, form, change)