from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AssignmentGroup, Task
from django.utils.translation import gettext_lazy as _

# Customizing the admin page for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    
    # Fields to be shown in the forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions')

# Register the CustomUser model with the custom admin page
admin.site.register(CustomUser, CustomUserAdmin)

# Register the AssignmentGroup model
@admin.register(AssignmentGroup)
class AssignmentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('members',)

# Register the Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_token', 'title', 'assignment_group', 'status', 'priority', 'created_at', 'assigned_to')
    list_filter = ('status', 'priority', 'assignment_group')
    search_fields = ('task_token', 'title', 'assignment_group__name', 'assigned_to')
    ordering = ('-created_at',)
    readonly_fields = ('task_token', 'created_at', 'updated_at')

    # Customizing the Task form for better usability
    fieldsets = (
        (None, {'fields': ('task_token', 'title', 'description', 'due_date', 'priority', 'status', 'assignment_group', 'creator', 'assigned_to')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
