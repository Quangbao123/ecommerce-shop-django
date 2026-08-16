from django.urls import path
from . import views

urlpatterns=[
    path('account/add-product/', views.add_product_view, name='add_product'),
    path('account/my-product/', views.display_product_view, name='my_product'),
    path('account/edit-product/<int:id>', views.edit_product_view, name='edit_product'),
    path('account/delete-product/<int:id>', views.delete_product_view, name='delete_product'),
    path('product/detail/<int:id>', views.product_detail_view, name='product_detail'),
    path('product/search/', views.search_view, name='product_search'),
    path('products/search_ajax', views.searchAjax_view, name='search_ajax'),
    path('products/search_reload', views.searchReload_view, name='search_reload'),
]