from django.db import models
from blogs.models import Category
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Product Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_default_product_category():
    product_category, created = ProductCategory.objects.get_or_create(name="uncategorized")
    return product_category.pk


class Brand(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_DEFAULT, default=get_default_product_category, related_name="Brands")
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ( {self.category} )"


def get_default_product_brand():
    product_brand, created = Brand.objects.get_or_create(name="No Brand")
    return product_brand.pk


class Product(models.Model):
    AVAILABILITY_CHOICES = (
        ('in stock', 'In Stock'),
        ('out of stock', 'Out of Stock')
    )
    product_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MyProducts")
    brand = models.ForeignKey(Brand, on_delete=models.SET_DEFAULT, default=get_default_product_brand, related_name="Products")
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/")
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=100, choices=AVAILABILITY_CHOICES, default='In Stock')
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    published_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    @property
    def discounted_price(self):
        if self.discount and self.discount > 0:
            return self.price - (self.price * self.discount // 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_amount(self):
        total = self.product.discounted_price * self.quantity
        return total
    
    class Meta:
        unique_together = ["customer", "product"]

    def __str__(self):
        return self.product.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100, default="Pakistan")
    province = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(20)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name}'s address"


class Order(models.Model):
    STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('PACKED', 'Packed'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Order")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="addresses", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='PENDING')
    bill = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.owner.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="OrderItems")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="PurchasedProducts")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["order", "item"]

    def __str__(self):
        return self.item.name