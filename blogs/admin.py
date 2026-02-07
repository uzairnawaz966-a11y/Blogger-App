from django.contrib import admin
from blogs.models import (
    Blog,
    Category,
    Interest,
    Follow,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]

    prepopulated_fields = {
    "slug": ("name", )
    }


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "category"
    ]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "category",
        "title",
        "description",
        "favourite",
        "slug",
        "published_at",
        "last_modified",
    ]

    prepopulated_fields = {
        "slug": ("title", )
    }


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "follower",
        "following"
    ]



# username: admin
# email: admin123@gmail.com
# password: samplepassword