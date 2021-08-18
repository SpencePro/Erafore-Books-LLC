from django.urls import path
from . import views

urlpatterns = [
    # path('', views.check_series, name='check'),
    # path('series_update', views.send_series_update, name='series'),
    path('new_book', views.new_book_notification, name='book'),
    path('sales', views.send_sales_notification, name='sales'),
    path('verify', views.verify_account, name='verify'),
    path('change', views.change_password, name='change'),
]
