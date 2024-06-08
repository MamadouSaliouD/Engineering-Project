from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    # Provide unique related_name attributes for groups and user_permissions 
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Use a unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Use a unique related_name
    )


class AssignmentGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assignment_groups_set')

    def __str__(self):
        return self.name

class Task(models.Model):
    task_token = models.CharField(max_length=8, unique=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    PRIORITY_CHOICES = [
        ("P1", "P1-Very High"),
        ("P2", "P2-High"),
        ("P3", "P3-Medium"),
        ("P4", "P4-Low"),
    ]
    priority = models.CharField(max_length=20, choices= PRIORITY_CHOICES, default='P3' )
    STATUS_CHOICES = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Done", "Done")
    ]
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default="New")
    assignment_group = models.ForeignKey(AssignmentGroup, related_name='tickets', on_delete=models.CASCADE, blank=False, null=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.task_token:
            last_task = Task.objects.all().order_by('id').last()
            if last_task:
                new_id = int(last_task.task_token[2:]) + 1
            else:
                new_id = 1
            self.task_token = 'TS{:06d}'.format(new_id)
        super(Task, self).save(*args, **kwargs)

