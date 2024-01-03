from django.contrib import admin
from mainapp.models import Book, Series, LoreObject, World
import csv
from django.http import HttpResponse

def export_selected_books(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'title', 'cover_artist', 'image', 'series', 'world', 'amazon_link', 'date_released', 'synopsis', 'on_sale', 'audio_book'])

    for book in queryset:
        writer.writerow([book.id, book.title, book.cover_artist, book.image, book.series, book.world, book.amazon_link, book.date_released, book.synopsis, book.on_sale, book.audio_book])

    return response

class BookAdmin(admin.ModelAdmin):
    actions = [export_selected_books]

def export_selected_series(modeladmin, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=series_data.csv"

        writer = csv.writer(response)
        writer.writerow(["id", "name", "description", "world", "date_started"])
        for obj in queryset:
            writer.writerow([obj.id, obj.name, obj.description, obj.world, obj.date_started])

        return response

class SeriesAdmin(admin.ModelAdmin):
    actions = [export_selected_series]

def export_selected_worlds(modeladmin, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=world_data.csv"

        writer = csv.writer(response)
        writer.writerow(["id", "name", "description"])
        for obj in queryset:
            writer.writerow([obj.id, obj.name, obj.description])

        return response

class WorldAdmin(admin.ModelAdmin):
    actions = [export_selected_worlds]

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(LoreObject)
admin.site.register(World, WorldAdmin)
