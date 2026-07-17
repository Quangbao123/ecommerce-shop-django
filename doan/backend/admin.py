from django.contrib import admin
from .models import CustomUser, Country, Blog

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'avatar', 'first_name', 'last_name', 'id_country')
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'author', 'created_at')