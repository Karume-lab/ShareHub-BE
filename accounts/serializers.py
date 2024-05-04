from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from core import serializers as core_ser
from . import models


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = models.CustomUser
        fields = ("id", "email", "password")


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = "__all__"
