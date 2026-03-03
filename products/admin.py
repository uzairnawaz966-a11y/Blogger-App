from django.contrib import admin
from products.models import (
    ProductCategory,
    Brand,
    Product,
    Cart,
    Order,
    OrderItem,
    Address,
    StripeOrderObject
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'category',
    ]
    prepopulated_fields = {
        'slug': ('name', )
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product_seller',
        'brand',
        'name',
        'description',
        'price',
        'discounted_price',
        'stock',
        'discount',
        'image',
        'availability',
        'modified_at',
        'published_at',
    ]
    prepopulated_fields = {
        'slug': ('name', )
    }


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        'seller',
        'customer',
        'product',
        'quantity',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'owner',
        'status',
        'bill',
        "is_paid",
        'address',
        'created_at',
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order',
        'item',
        'quantity',
        'total_price',
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'full_name',
        'phone',
        'country',
        'province',
        'street_address',
        'postal_code',
    ]

@admin.register(StripeOrderObject)
class StripeOrderObjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "payment_intent_id",
        "is_refunded",
        "created_at",
    ]