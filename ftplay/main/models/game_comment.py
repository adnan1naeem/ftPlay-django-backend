from django.db import models
from .base import Base

class GameComment(Base):
    content = models.TextField()
    
    player = models.ForeignKey(
        'Player',
        on_delete=models.SET_NULL,
        null=True,
        related_name='game_comments'
    )
    
    organizer = models.ForeignKey(
        'Organizer',
        on_delete=models.SET_NULL,
        null=True
    )
    
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return f"Comment on {self.game.title}" 