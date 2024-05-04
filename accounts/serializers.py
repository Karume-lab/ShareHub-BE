from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "password")


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = "__all__"
