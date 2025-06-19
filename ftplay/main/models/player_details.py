from django.db import models
from .base import Base

class PlayerDetails(Base):
    age_group = models.CharField(max_length=50, null=True, blank=True)
    play_position = models.JSONField(null=True, blank=True)  # Array of positions
    trait_that_suits = models.JSONField(null=True, blank=True)  # Array of traits
    skill_level = models.CharField(max_length=50, null=True, blank=True)
    often_play_football = models.CharField(max_length=50, null=True, blank=True)
    
    rank_technique_score = models.IntegerField(default=0)
    rank_physical_score = models.IntegerField(default=0)
    rank_defense_score = models.IntegerField(default=0)
    rank_attack_score = models.IntegerField(default=0)
    
    video_link = models.CharField(max_length=255, null=True, blank=True)
    video_key = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    
    wins = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    
    player = models.OneToOneField(
        'Player',
        on_delete=models.CASCADE,
        related_name='details'
    )

    @property
    def win_percentage(self):
        total = (self.wins or 0) + (self.draw or 0) + (self.lose or 0)
        if total == 0:
            return 0
        return ((self.wins or 0) / total) * 100

    def __str__(self):
        return f"Details for {self.player.name}" 