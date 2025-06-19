from django.db import models
from .base import Base

class Game(Base):
    title = models.CharField(max_length=255)
    images = models.JSONField()  # Array of image URLs
    time = models.DateTimeField()
    date = models.DateField()
    region = models.CharField(max_length=50, default='UTC')
    venue_details = models.JSONField()  # Array of venue details
    location = models.JSONField(null=True, blank=True)  # Array of location details
    duration = models.IntegerField(null=True, blank=True)
    number_of_participants = models.IntegerField()
    player_fees = models.DecimalField(max_digits=10, decimal_places=2)
    game_rules = models.TextField()
    
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='UPCOMING'
    )
    
    VISIBILITY_CHOICES = [
        ('PRIVATE', 'Private'),
        ('PUBLIC', 'Public'),
    ]
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PRIVATE'
    )
    
    password = models.CharField(max_length=255, null=True, blank=True)
    
    # Relationships
    organizer = models.ForeignKey(
        'Organizer',
        on_delete=models.CASCADE,
        related_name='games'
    )
    
    participants = models.ManyToManyField(
        'Player',
        related_name='games'
    )

    def __str__(self):
        return self.title 