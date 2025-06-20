from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
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

    def get_game_datetime(self):
        """Get the combined date and time of the game"""
        return datetime.combine(self.date, self.time.time())

    def get_game_end_datetime(self):
        """Get the end time of the game (start time + duration)"""
        game_start = self.get_game_datetime()
        if self.duration:
            return game_start + timedelta(minutes=self.duration)
        # Default 2 hours if no duration specified
        return game_start + timedelta(hours=2)

    def should_be_ongoing(self):
        """Check if game should be marked as ongoing"""
        now = timezone.now()
        game_start = timezone.make_aware(self.get_game_datetime())
        return game_start <= now < timezone.make_aware(self.get_game_end_datetime())

    def should_be_completed(self):
        """Check if game should be marked as completed"""
        now = timezone.now()
        game_end = timezone.make_aware(self.get_game_end_datetime())
        return now >= game_end

    def update_status(self):
        """Update game status based on current time"""
        if self.status == 'CANCELED':
            return False  # Don't update canceled games
        
        if self.should_be_completed():
            if self.status != 'COMPLETED':
                self.status = 'COMPLETED'
                self.save(update_fields=['status', 'updated_at'])
                return True
        elif self.should_be_ongoing():
            if self.status != 'ONGOING':
                self.status = 'ONGOING'
                self.save(update_fields=['status', 'updated_at'])
                return True
        
        return False

    @classmethod
    def update_all_game_statuses(cls):
        """Update status of all games based on current time"""
        updated_games = []
        
        # Get all non-canceled games
        games = cls.objects.exclude(status='CANCELED')
        
        for game in games:
            if game.update_status():
                updated_games.append(game)
        
        return updated_games

    def is_completed(self):
        """Check if game is completed"""
        return self.status == 'COMPLETED'

    def is_ongoing(self):
        """Check if game is ongoing"""
        return self.status == 'ONGOING'

    def is_upcoming(self):
        """Check if game is upcoming"""
        return self.status == 'UPCOMING'

    def is_canceled(self):
        """Check if game is canceled"""
        return self.status == 'CANCELED' 