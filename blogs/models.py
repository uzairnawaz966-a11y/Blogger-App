from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def default_category():
    category, created = Category.objects.get_or_create(name="No Category")
    return category


class Interest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="interest")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=default_category)


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=default_category, related_name="blogs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    favourite = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ( {self.category.name} )"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)