from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.models import Player, Organizer

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['PLAYER', 'ORGANIZER'])
    name = serializers.CharField()
    gender = serializers.ChoiceField(choices=['MALE', 'FEMALE', 'OTHER'], required=False)
    image = serializers.CharField(required=False, allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        name = validated_data.pop('name')
        gender = validated_data.pop('gender', None)
        image = validated_data.pop('image', None)

        # Create the user
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        # Create either Player or Organizer based on user_type
        if user_type == 'PLAYER':
            Player.objects.create(
                user=user,
                name=name,
                gender=gender,
                image=image
            )
        else:
            Organizer.objects.create(
                user=user,
                name=name,
                gender=gender,
                image=image
            )

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value 