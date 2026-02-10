from django import forms
from blogs.models import Category
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    confirmation_password = forms.CharField(max_length=16)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Choose your favourite categories")

    class Meta:
        model = User
        fields =  [
            "username",
            "email",
            "password",
        ]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': "choose a strong password"}),
            "confirmation_password": forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirmation_password = cleaned_data.get("confirmation_password")

        if password and confirmation_password:
            if password != confirmation_password:
                raise forms.ValidationError("Passwords does not match. Please make sure that the password and confirmation password match")
        return cleaned_data