from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from common.models import BaseModel




class UserManager(BaseUserManager):
    """
    Custom manager for the UserModel.
 
    """
    def _create_user(self, email, username, phone_number, password, **extra_fields):
        """
        email, username, phone_number, and password.
        Handles basic validation and password hashing.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not phone_number:
             raise ValueError('Users must have a phone number')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db) 
        return user

    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        """
        Creates and saves a regular 'normal' User.
        Normal users are NOT staff and NOT superusers by default.
        
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, username, phone_number, password, **extra_fields)

    def create_superuser(self, email, username, phone_number, password, **extra_fields):
        """
        Creates and saves an 'admin' User (Superuser).
    
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

   
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, phone_number, password, **extra_fields)





class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User Model.
    Uses UserManager to handle creation of normal vs admin users.
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True, 
        help_text='Required. Used for login.'
    )
    username = models.CharField(
        max_length=150,
        unique=True, 
        help_text='Required. 150 characters or fewer.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Required.'
    )

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into the Django admin site.',
    )
    is_active = models.BooleanField(
        default=True, 
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
    )


    objects = UserManager()

   
    EMAIL_FIELD = 'email' 
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'phone_number'] 

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username'] 

    def __str__(self):
        return self.email 

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
