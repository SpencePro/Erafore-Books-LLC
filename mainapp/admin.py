from django.contrib import admin
from mainapp.models import Book, Series, LoreObject
# Register your models here.
admin.site.register(Book)
admin.site.register(Series)
admin.site.register(LoreObject)

