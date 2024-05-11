from rest_framework import serializers
from accounts import serializers as accounts_serializers
from . import models


class Innovation(serializers.ModelSerializer):
    author = accounts_serializers.Author(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = models.Innovation
        fields = (
            "url",
            "title",
            "author",
            "description",
            "dashboard_link",
            "dashboard_image",
            "banner_image",
            "comments_number",
            "likes_number",
            "created_at",
            "updated_at",
            "is_liked",
            "is_bookmarked",
            "status",
            "category",
        )

    def get_is_liked(self, obj):
        try:
            author = self.context.get("request").user.user_profile
            is_liked = obj.get_is_liked(author)
        except AttributeError:
            is_liked = None
        return is_liked

    def get_is_bookmarked(self, obj):
        try:
            author = self.context.get("request").user.user_profile
            is_bookmarked = obj.get_is_bookmarked(author)
        except AttributeError:
            is_bookmarked = None
        return is_bookmarked


class Like(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = (
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
