from django.db import models
from users.models import CustomUser
# Create your models here.
class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    