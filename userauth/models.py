from django.db import models
from django.contrib.auth.models import User
from blogs.models import Category


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_interests")
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user}'s Interest"