from django import forms
from products.models import Product, Cart, Address


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'price',
            'discount',
            'stock',
            'brand',
        ]


class QuantityForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "country",
            "province",
            "street_address",
            "postal_code",
        ]
        labels = {
            "postal_code": "Postal Code",
        }