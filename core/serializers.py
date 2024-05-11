from rest_framework import serializers
from accounts import serializers as accounts_serializers
from . import models


class Innovation(serializers.ModelSerializer):
    author = accounts_serializers.Author(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Innovation
        fields = (
            "url",
            "title",
            "author",
            "description",
            "dashboard_link",
            "dashboard_image",
            "created_at",
            "updated_at",
            "is_liked",
            "status",
            "category",
        )

    def get_is_liked(self, obj):
        try:
            author = self.context.get("request").user.user_profile
            is_liked = obj.get_is_liked(author)
        except AttributeError:
            is_liked = False
        return is_liked


class Like(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = (
            "url",
            "author",
            "innovation",
        )
        read_only_fields = (
            "author",
            "innovation",
        )


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
            "text",
            "created_at",
            "updated_at",
        )
