from rest_framework import serializers
from main.models import Player, PlayerDetails

class PlayerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerDetails
        fields = [
            'age_group', 'play_position', 'trait_that_suits', 'skill_level',
            'often_play_football', 'rank_technique_score', 'rank_physical_score',
            'rank_defense_score', 'rank_attack_score', 'video_link', 'video_key',
            'title', 'location', 'wins', 'draw', 'lose', 'goal', 'assists'
        ]

class PlayerProfileSerializer(serializers.ModelSerializer):
    details = PlayerDetailsSerializer(required=False)
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = [
            'id', 'name', 'image', 'gender', 'user_type', 'details'
        ]
        read_only_fields = ['id']

    def get_user_type(self, obj):
        return 'PLAYER'

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        
        # Update Player fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create PlayerDetails
        if details_data:
            details, created = PlayerDetails.objects.get_or_create(player=instance)
            for attr, value in details_data.items():
                setattr(details, attr, value)
            details.save()

        return instance

class PlayerProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    image = serializers.CharField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=['MALE', 'FEMALE', 'OTHER'], required=False)
    
    # Player Details fields
    age_group = serializers.CharField(required=False, allow_null=True)
    play_position = serializers.ListField(required=False, allow_null=True)
    trait_that_suits = serializers.ListField(required=False, allow_null=True)
    skill_level = serializers.CharField(required=False, allow_null=True)
    often_play_football = serializers.CharField(required=False, allow_null=True)
    video_link = serializers.CharField(required=False, allow_null=True)
    video_key = serializers.CharField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)

    # Rank Score fields
    rank_technique_score = serializers.IntegerField(min_value=0, max_value=100, required=False)
    rank_physical_score = serializers.IntegerField(min_value=0, max_value=100, required=False)
    rank_defense_score = serializers.IntegerField(min_value=0, max_value=100, required=False)
    rank_attack_score = serializers.IntegerField(min_value=0, max_value=100, required=False)

    def update(self, instance, validated_data):
        # Update Player fields
        player_fields = ['name', 'image', 'gender']
        player_data = {k: v for k, v in validated_data.items() if k in player_fields}
        for attr, value in player_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update PlayerDetails fields
        details_fields = [
            'age_group', 'play_position', 'trait_that_suits', 'skill_level',
            'often_play_football', 'video_link', 'video_key', 'title', 'location',
            'rank_technique_score', 'rank_physical_score', 'rank_defense_score', 'rank_attack_score'
        ]
        details_data = {k: v for k, v in validated_data.items() if k in details_fields}
        
        if details_data:
            details, created = PlayerDetails.objects.get_or_create(player=instance)
            for attr, value in details_data.items():
                setattr(details, attr, value)
            details.save()

        return instance

class PlayerRankScoreUpdateSerializer(serializers.Serializer):
    rank_technique_score = serializers.IntegerField(min_value=0, max_value=100)
    rank_physical_score = serializers.IntegerField(min_value=0, max_value=100)
    rank_defense_score = serializers.IntegerField(min_value=0, max_value=100)
    rank_attack_score = serializers.IntegerField(min_value=0, max_value=100)

    def update(self, instance, validated_data):
        details, created = PlayerDetails.objects.get_or_create(player=instance)
        for attr, value in validated_data.items():
            setattr(details, attr, value)
        details.save()
        return instance

class PlayerDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value 