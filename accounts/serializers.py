from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from . import models


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = models.CustomUser
        fields = ("id", "email", "password")


class UserProfile(serializers.HyperlinkedModelSerializer):
    email = serializers.StringRelatedField()
    innovations = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="innovation-detail"
    )

    class Meta:
        model = models.UserProfile
        fields = (
            "url",
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "bio",
            "profile_picture",
            "innovations",
        )
