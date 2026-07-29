from django.contrib import admin
from .models import Blog, Comment, Rate

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'content', 'image', 'created_at')
@admin.register(Comment)
class CommendAdmin(admin.ModelAdmin):
    list_display = ('comment', 'id_blog', 'id_user', 'user_name', 'level', 'created_at')
@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('rate', 'id_blog', 'id_user', 'rated_at')