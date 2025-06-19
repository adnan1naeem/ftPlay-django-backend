from django.db import models
from .base import Base

class Notification(Base):
    NOTIFICATION_TYPE_CHOICES = [
        ('GAME_CREATED', 'Game Created'),
        ('GAME_JOINED', 'Game Joined'),
        ('GAME_COMMENT', 'Game Comment'),
        ('GAME_RATING', 'Game Rating'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('PAYMENT_COMPLETED', 'Payment Completed'),
        ('RATING_VERIFICATION', 'Rating Verification'),
        ('NEW_PARTICIPANT', 'New Participant'),
        ('GAME_STARTING_SOON', 'Game Starting Soon'),
        ('GAME_COMPLETED', 'Game Completed'),
        ('PLAYER_RATED_GAME', 'Player Rated Game'),
        ('GAME_DELETED', 'Game Deleted'),
        ('GAME_CANCELED', 'Game Canceled'),
        ('NEW_COMMENT', 'New Comment'),
        ('RATING_SUBMITTED', 'Rating Submitted'),
        ('RATING_VERIFIED', 'Rating Verified'),
        ('PAYMENT_REFUNDED', 'Payment Refunded'),
    ]
    
    type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    recipient_player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        null=True,
        related_name='notifications'
    )
    
    recipient_organizer = models.ForeignKey(
        'Organizer',
        on_delete=models.CASCADE,
        null=True,
        related_name='notifications'
    )
    
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    actor_player = models.ForeignKey(
        'Player',
        on_delete=models.SET_NULL,
        null=True,
        related_name='actor_notifications'
    )
    
    actor_organizer = models.ForeignKey(
        'Organizer',
        on_delete=models.SET_NULL,
        null=True,
        related_name='actor_notifications'
    )

    def __str__(self):
        return f"{self.type} notification for {self.game.title}" 