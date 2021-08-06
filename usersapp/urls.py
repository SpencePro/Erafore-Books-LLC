from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('reset<int:id>', views.reset_password, name='reset'),
    path('delete<int:id>', views.delete_account, name='delete'),
    #path('change_email<int:id>', views.change_email, name='change_email'),
    path('edit_settings', views.edit_settings, name='edit'),
    path('profile/<username>', views.profile_view, name='profile'),
    path('add/<int:id>', views.add_to_wishlist, name='add'),
    path('follow/<int:id>', views.follow_series, name='follow'),
]
