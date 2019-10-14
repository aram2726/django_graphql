from django.db import models

from apps.movie.models import Movie


class Hero(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=(('M', 'Male'), ('F', 'Female')), default='F')
    movie = models.ForeignKey(Movie, blank=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "movie"),)
