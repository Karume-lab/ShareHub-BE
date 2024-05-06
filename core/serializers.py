from rest_framework import serializers
from accounts import serializers as accounts_serializers
from . import models
1

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
        )
