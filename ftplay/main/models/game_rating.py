from django.db import models
from .base import Base

class GameRating(Base):
    RESULT_CHOICES = [
        ('WIN', 'Win'),
        ('LOSE', 'Lose'),
        ('DRAW', 'Draw'),
    ]
    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES
    )
    
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    
    VERIFICATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
    ]
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_STATUS_CHOICES,
        default='PENDING'
    )
    
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        related_name='game_ratings'
    )
    
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self):
        return f"Rating for {self.game.title} by {self.player.name}" 