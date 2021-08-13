from django.db import models
from django.contrib.auth.models import AbstractUser

from mainapp.models import Book, Series


class User(AbstractUser):
    can_send_sales = models.BooleanField(default=True)
    can_send_updates = models.BooleanField(default=True)
    can_send_new = models.BooleanField(default=True)
    can_send_wish_sales = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
