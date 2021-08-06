from django.contrib import admin
from usersapp.models import User, Follow, Wish

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Wish)
