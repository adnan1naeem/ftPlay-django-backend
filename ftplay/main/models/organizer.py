from django.db import models
from .base import Base
from .user import CustomUser

class Organizer(Base):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='organizer')
    name = models.CharField(max_length=100)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name 