from rest_framework import serializers
from . import models


class Innovation(serializers.ModelSerializer):
    class Meta:
        model = models.Innovation
        fields = (
            "author",
            "title",
            "description",
            "dataset",
            "created_at",
            "updated_at",
            "status",
            "categories",
            "slug",
        )
