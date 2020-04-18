from django.shortcuts import render
from django.http import JsonResponse

from api import models
from api import serializers


def film_list(request):
    if request.method == 'GET':
        films = models.Film.objects.all()
        serializer = serializers.FilmSerializer(films, many=True)
        return JsonResponse(serializer.data, safe=False)
