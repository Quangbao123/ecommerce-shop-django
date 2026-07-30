from django.urls import path
from . import views

urlpatterns=[
    path('account/add-product/', views.add_product_view, name='add_product')
]