from django.db import models

# Create your models here.
from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class PostModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)