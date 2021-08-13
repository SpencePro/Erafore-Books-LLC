from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('verify_registration', views.verify_registration, name="verify_registration"),
    path('reset', views.reset_password, name='reset'),
    path('verify_reset', views.verify_reset, name='verify_reset'),
    path('delete/<int:id>', views.delete_account, name='delete'),
    path('edit_settings', views.edit_settings, name='edit'),
    path('profile/<int:id>', views.profile_view, name='profile'),
    path('add/<int:id>', views.add_to_wishlist, name='add'),
    path('follow/<int:id>', views.follow_series, name='follow'),
]
