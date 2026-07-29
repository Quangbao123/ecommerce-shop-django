from django.urls import path
from . import views
urlpatterns = [
    path('blog/', views.blog_list_view, name='blog_list'),
    path('blog/<int:id>/', views.blog_detail_view, name='blog_detail'),
    path('blog/rate/', views.blog_rating_view, name='blog_detail_rate'),
    path('blog/comment/', views.blog_comment_view, name='blog_detail_comment')
]