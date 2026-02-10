from django.db import models
from django.contrib.auth.models import User
from blogs.models import Blog



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["follower", "following"]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class BlogRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_ratings")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="ratings")
    comment = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["user", "blog"]

    def __str__(self):
        return self.blog.title