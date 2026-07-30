from django.db import models
from users.models import CustomUser

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.IntegerField()
    sale = models.IntegerField(default=0)
    company = models.CharField(max_length=50)
    image = models.JSONField(default=list)
    detail = models.TextField()
