from django import forms
from blogs.models import Blog


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