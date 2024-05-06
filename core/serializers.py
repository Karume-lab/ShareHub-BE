from rest_framework import serializers
from accounts import serializers as accounts_serializers
from . import models


class Innovation(serializers.ModelSerializer):
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
        )
