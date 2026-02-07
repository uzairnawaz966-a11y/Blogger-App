from django import forms
from blogs.models import Blog, Interest, Category
from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "category",
            "title",
            "description",
            "favourite"
        ]
        widgets = {
            "address": (forms.TextInput(attrs={'placeholder': 'Add your blog url here'}))
        }
        labels = {
            "favourite": "Add to Favourite"
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["category"]


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
    
class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ["category"]
        labels = {
            "category": "Your Interested Category"
        }