from django.contrib import admin
from mainapp.models import Book, Series, LoreObject, World
# Register your models here.
admin.site.register(Book)
admin.site.register(Series)
admin.site.register(LoreObject)
admin.site.register(World)

