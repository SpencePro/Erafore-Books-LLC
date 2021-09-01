from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.all_books_view, name='all_books'),
    path('filter_books', views.filter_books, name='filter_books'),
    path('book/<int:id>', views.book_view, name='book'),
    path('contact', views.contact_view, name='contact'),
    path('lore', views.lore_view, name='lore_page'),
    path('lore_object/<int:id>', views.lore_object_view, name='lore_object'),
    path('search', views.search_view, name='search'),
    path('random', views.random_view, name='random'),
    path('back', views.back_page, name='back'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")))
]
