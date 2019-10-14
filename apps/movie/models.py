from django.db import models


class Movie(models.Model):
    name = models.CharField("name", blank=False, max_length=100)
