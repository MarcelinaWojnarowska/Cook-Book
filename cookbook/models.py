from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Recipe(models.Model):

    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    preparing = models.TextField()
    date_added = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



