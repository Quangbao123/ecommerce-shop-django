from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    id_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)