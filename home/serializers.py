from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class META:
        model = Image
        fields = ['name', 'type', 'url', ]
