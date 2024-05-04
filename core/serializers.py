from rest_framework import serializers
from . import models


class Innovation(serializers.ModelSerializer):
    class Meta:
        model = models.Innovation
        fields = "__all__"
