from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    image = models.ImageField(upload_to='images/', default='images/eat.png')
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    preparing = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
