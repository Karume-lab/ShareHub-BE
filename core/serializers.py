from rest_framework import serializers
from accounts import serializers as accounts_serializers
from . import models


class Innovation(serializers.ModelSerializer):
    author = accounts_serializers.Author(read_only=True)

    class Meta:
        model = models.Innovation
        fields = (
            "url",
            "title",
            "author",
            "description",
            "dataset",
            "created_at",
            "updated_at",
            "status",
            "category",
            "likes",
        )


class BaseComment(serializers.ModelSerializer):
    author = accounts_serializers.Author()

    class Meta:
        model = models.BaseComment
        fields = ("author", "text", "created_at", "updated_at", "likes")
        read_only_fields = ("created_at", "updated_at", "likes")


class InnovationComment(serializers.ModelSerializer):
    innovation = serializers.PrimaryKeyRelatedField(
        queryset=models.Innovation.objects.all()
    )
    author = accounts_serializers.Author(read_only=True)

    class Meta:
        model = models.InnovationComment
        fields = (
            "innovation",
            "author",
        ) + BaseComment.Meta.fields
