from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from . import models


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = models.CustomUser
        fields = (
            "id",
            "email",
            "password",
        )


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = (
            "url",
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "created_at",
            "updated_at",
            "bio",
            "profile_picture",
            "linked_in_url",
            "x_in_url",
            "superset_url",
        )


class Author(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "profile_picture",
        )
