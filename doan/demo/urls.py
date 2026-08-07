from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('add-to-cart/<int:id>', views.add_to_cart_view, name='add_product_to_cart'),
    path('view-cart', views.view_product_cart, name='view_product_cart')
]