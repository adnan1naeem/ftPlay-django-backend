from rest_framework import serializers
from main.models import Game, GameRating, GameComment

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'images', 'time', 'date', 'region',
            'venue_details', 'location', 'duration', 'number_of_participants',
            'player_fees', 'game_rules', 'status', 'visibility', 'password',
            'organizer', 'participants'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class GameRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRating
        fields = [
            'id', 'result', 'goals', 'assists',
            'verification_status', 'player', 'game'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class GameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameComment
        fields = ['id', 'content', 'player', 'organizer', 'game']
        read_only_fields = ['id', 'created_at', 'updated_at'] 