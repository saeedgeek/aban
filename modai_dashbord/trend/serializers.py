from rest_framework import serializers
from .models import Tracks


class TracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracks
        fields = '__all__'
