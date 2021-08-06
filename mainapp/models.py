from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField, EmailField
from django.db.models.fields.related import ForeignKey


class Series(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_started = models.DateField()
    world = models.CharField(max_length=255, null=True, blank=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    cover_artist = models.CharField(max_length=255)
    date_released = models.DateField()
    image = models.CharField(max_length=255, null=True, blank=True)
    amazon_link = models.URLField(max_length=255, blank=True, null=True)


class LoreObject(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    world = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)



