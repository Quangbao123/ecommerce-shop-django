from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name = 'user_register'),
    path('login/', views.login_view, name = 'user_login'),
    path('logout/', views.custom_logout, name = 'custom_logout'),
    path('account/update', views.update_account_view, name='account_update'),
    path('forgot-pass/', views.forgot_pass_view, name='forgot_password'),
    path('renew-pass/', views.renew_password_view, name='renew_password'),
]