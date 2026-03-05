from django.contrib import admin
from userauth.models import Interest, StripeCustomer

# Register your models here.





@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
    ]


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user__username",
        'stripe_customer_id',
    ]


# username: admin
# email: admin123@gmail.com
# password: samplepassword