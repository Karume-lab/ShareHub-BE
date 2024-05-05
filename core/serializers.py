from rest_framework import serializers
from . import models


class Innovation(serializers.HyperlinkedModelSerializer):
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
