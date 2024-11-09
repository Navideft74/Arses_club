from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from datetime import timedelta
from .myuser_manager import MyUserManager

class MyUser(AbstractUser, PermissionsMixin):
    # Remove unused fields from the base AbstractUser
    username = None
    first_name = None
    last_name = None
    email = None

    # Use mobile as the unique identifier for login
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)  # Stores OTP as a 4-digit positive integer
    otp_created = models.DateTimeField(blank=True, null=True)  # Timestamp for when OTP was generated

    # Specify custom manager for user creation
    objects = MyUserManager()

    # Set mobile as the unique identifier field
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    # Specify custom backend for authentication
    backend = 'accounts.mybackend.MobileBackend'

    def __str__(self):
        # Return profile's full name if available, otherwise return mobile number
        if hasattr(self, 'profile') and self.profile.first_name and self.profile.last_name:
            return f'{self.profile.first_name} {self.profile.last_name}'
        return self.mobile

    def otp_is_valid(self, expiration_minutes=3):
        """
        Check if the OTP is still valid based on expiration time.
        
        Args:
            expiration_minutes (int): The time window in minutes within which the OTP is valid.
            
        Returns:
            bool: True if OTP is valid, False otherwise.
        """
        if not self.otp_created:
            print("Debug: OTP creation time not found.")  # Debug: No OTP creation time
            return False
        # Calculate if the OTP is within the valid time frame
        is_valid = timezone.now() - self.otp_created < timedelta(minutes=expiration_minutes)
        print(f"Debug: OTP valid for {self.mobile}? {is_valid}")  # Debug: Print OTP validity
        return is_valid


class Profile(models.Model):
    # One-to-one relationship to the MyUser model with cascade deletion
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional profile picture

    def __str__(self):
        # Return the full name of the user for easy identification
        return f'{self.first_name} {self.last_name}'
