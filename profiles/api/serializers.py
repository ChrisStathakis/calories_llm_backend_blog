from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg
from rest_framework_simplejwt.tokens import RefreshToken, Token

from profiles.models import Profile, TargetCalories

import datetime

User = get_user_model()

class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ["user", "height", "weight", "activity_lvl", "year_of_birth", "calories", "bmr", "age", "gender", "id"]

class TargetCaloriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TargetCalories
        fields = ['calories', 'profile', 'target', 'protein']

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):

        username_exists = User.objects.filter(username=data['username']).exists()
        email_exists = User.objects.filter(email=data['email']).exists()
        if username_exists or email_exists:
            raise serializers.ValidationError("Username or Email exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        refresh = RefreshToken.for_user(user)
        profile, created = Profile.objects.get_or_create(user=user)
        data = {
            'access_token': refresh.access_token,
            'refresh_token': str(refresh),
            'username': user.username,
            'email': user.email,
            'profile_id': profile.id
        }
        return data