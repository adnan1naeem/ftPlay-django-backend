from rest_framework import serializers
from main.models import Game, GameRating, GameComment
from django.utils import timezone
import datetime

class GameSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)
    participants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'images', 'time', 'date', 'region',
            'venue_details', 'location', 'duration', 'number_of_participants',
            'player_fees', 'game_rules', 'status', 'visibility', 'password',
            'organizer', 'organizer_name', 'participants', 'participants_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer', 'organizer_name']

    def get_participants_count(self, obj):
        return obj.participants.count()

class GameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'title', 'images', 'time', 'date', 'region',
            'venue_details', 'location', 'duration', 'number_of_participants',
            'player_fees', 'game_rules', 'visibility', 'password'
        ]

    def validate(self, data):
        """Custom validation for game creation"""
        # Validate that date and time are in the future
        if 'date' in data and 'time' in data:
            game_datetime = datetime.datetime.combine(data['date'], data['time'].time())
            # Make the datetime timezone-aware
            game_datetime = timezone.make_aware(game_datetime)
            if game_datetime <= timezone.now():
                raise serializers.ValidationError("Game date and time must be in the future")
        
        # Validate number of participants
        if 'number_of_participants' in data and data['number_of_participants'] <= 0:
            raise serializers.ValidationError("Number of participants must be greater than 0")
        
        # Validate player fees
        if 'player_fees' in data and data['player_fees'] < 0:
            raise serializers.ValidationError("Player fees cannot be negative")
        
        # Validate duration
        if 'duration' in data and data['duration'] is not None and data['duration'] <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        
        return data

class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'title', 'images', 'time', 'date', 'region',
            'venue_details', 'location', 'duration', 'number_of_participants',
            'player_fees', 'game_rules', 'visibility', 'password'
        ]

    def validate(self, data):
        """Custom validation for game updates"""
        instance = self.instance
        
        # Don't allow updates if game is completed or canceled
        if instance.status in ['COMPLETED', 'CANCELED']:
            raise serializers.ValidationError("Cannot update a completed or canceled game")
        
        # Validate that date and time are in the future
        if 'date' in data and 'time' in data:
            game_datetime = datetime.datetime.combine(data['date'], data['time'].time())
            game_datetime = timezone.make_aware(game_datetime)
            if game_datetime <= timezone.now():
                raise serializers.ValidationError("Game date and time must be in the future")
        elif 'date' in data and instance.time:
            game_datetime = datetime.datetime.combine(data['date'], instance.time.time())
            game_datetime = timezone.make_aware(game_datetime)
            if game_datetime <= timezone.now():
                raise serializers.ValidationError("Game date and time must be in the future")
        elif 'time' in data and instance.date:
            game_datetime = datetime.datetime.combine(instance.date, data['time'].time())
            game_datetime = timezone.make_aware(game_datetime)
            if game_datetime <= timezone.now():
                raise serializers.ValidationError("Game date and time must be in the future")
        
        # Validate number of participants (can't be less than current participants)
        if 'number_of_participants' in data:
            current_participants = instance.participants.count()
            if data['number_of_participants'] < current_participants:
                raise serializers.ValidationError(
                    f"Cannot reduce participants below current count ({current_participants})"
                )
            if data['number_of_participants'] <= 0:
                raise serializers.ValidationError("Number of participants must be greater than 0")
        
        # Validate player fees
        if 'player_fees' in data and data['player_fees'] < 0:
            raise serializers.ValidationError("Player fees cannot be negative")
        
        # Validate duration
        if 'duration' in data and data['duration'] is not None and data['duration'] <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        
        return data

class GameRatingSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    
    class Meta:
        model = GameRating
        fields = [
            'id', 'result', 'goals', 'assists',
            'verification_status', 'player', 'player_name', 'game'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'verification_status']

class GameCommentSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.name', read_only=True)
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)
    
    class Meta:
        model = GameComment
        fields = ['id', 'content', 'player', 'player_name', 'organizer', 'organizer_name', 'game']
        read_only_fields = ['id', 'created_at', 'updated_at'] 