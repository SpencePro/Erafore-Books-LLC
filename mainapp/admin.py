from django.contrib import admin
from mainapp.models import Book, Series, LoreObject
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

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Series)
admin.site.register(LoreObject)
