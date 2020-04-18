from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    duration = models.CharField(max_length=5)
