from rest_framework import serializers
from main.models import Organizer

class OrganizerProfileSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Organizer
        fields = [
            'id', 'name', 'image', 'gender', 'user_type'
        ]

    def get_user_type(self, obj):
        return 'ORGANIZER'

class OrganizerProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'name', 'image', 'gender'
        ]

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()

class OrganizerDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value 