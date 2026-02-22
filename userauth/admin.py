from django.contrib import admin
from userauth.models import Interest

# Register your models here.





@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]


# username: admin
# email: admin123@gmail.com
# password: samplepassword