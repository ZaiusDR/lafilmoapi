from rest_framework import serializers
from api.models import Film


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'director', 'year', 'duration']
