from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import os
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
# class UserManager(BaseUserManager):
#     """Manager for user profiles."""

#     def create_user(self, email, password=None, **extra_fields):
#         """Create a new user profile."""
#         if not email:
#             raise ValueError('User must have an email address.')
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user


#     def create_superuser(self, email, password):
#         """Create and save a new superuser with given details."""
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user
  
# class User(AbstractBaseUser, PermissionsMixin):
#     """User in the system."""
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
     
class Entrys(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    json = models.CharField(max_length=10000000)
    project = models.ForeignKey(
        'Project',
        related_name='entries',
        on_delete=models.CASCADE
    )
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

# class Documentation(models.Model):
#     name = models.CharField(max_length=100)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     title = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

