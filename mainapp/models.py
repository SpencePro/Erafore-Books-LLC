from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField, EmailField
from django.db.models.fields.related import ForeignKey
import csv
from django.http import HttpResponse


class World(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Series(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_started = models.DateField()
    world = models.ForeignKey(World, default=None, on_delete=models.CASCADE)


class Book(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    cover_artist = models.CharField(max_length=255, null=True, blank=True)
    date_released = models.DateField()
    image = models.CharField(max_length=255, null=True, blank=True)
    amazon_link = models.URLField(max_length=255, null=True, blank=True)
    world = models.ForeignKey(World, default=None, on_delete=models.CASCADE)
    on_sale = models.BooleanField(default=False)
    audio_book = models.BooleanField(default=False)


class LoreObject(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, default=None, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, null=True, blank=True)


def export_selected_books(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'cover_artist', 'image', 'series', 'world', 'amazon_link', 'date_released', 'synopsis', 'on_sale', 'audio_book'])

    for book in queryset:
        writer.writerow([book.id, book.title, book.cover_artist, book.image, book.series, book.world, book.amazon_link, book.date_released, book.synopsis, book.on_sale, book.audio_book])

    return response
