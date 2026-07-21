from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name = 'user_register'),
    path('login/', views.login_view, name = 'user_login'),
    path('logout/', views.custom_logout, name = 'custom_logout'),
]