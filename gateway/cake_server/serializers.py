from rest_framework import serializers

from .models import Cake


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = ["id", "name", "comment", "imageUrl", "yumFactor"]
