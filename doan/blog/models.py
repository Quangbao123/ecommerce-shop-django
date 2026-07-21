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