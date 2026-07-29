from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import CustomUser

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog/images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Rate(models.Model):
    rate = models.IntegerField() # 1 - 5 rating-star
    id_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rated_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment = models.TextField()
    id_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
