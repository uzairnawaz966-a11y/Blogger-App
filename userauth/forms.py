from django import forms
from blogs.models import Category
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Choose your favourite category")
    
    class Meta:
        model = User
        fields =  [
            "username",
            "email",
            "password",
        ]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': "choose a strong password"})
        }