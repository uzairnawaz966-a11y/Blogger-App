from django.contrib import admin
from blogs.models import (
    Blog,
    Category,
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






# username: admin
# email: admin123@gmail.com
# password: samplepassword