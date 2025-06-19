from django.db import models
from .base import Base

class GamePayment(Base):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_payment_id = models.CharField(max_length=255, null=True, blank=True)
    
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        related_name='game_payments'
    )
    
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='payments'
    )

    def __str__(self):
        return f"Payment for {self.game.title} by {self.player.name}" 