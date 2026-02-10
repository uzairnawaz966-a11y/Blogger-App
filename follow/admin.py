from django.contrib import admin
from follow.models import Follow, BlogRating


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "follower",
        "following",
    ]


@admin.register(BlogRating)
class BlogRatingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "blog",
        "comment",
        "likes",
        "views",
    ]