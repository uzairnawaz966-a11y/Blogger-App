from django import forms
from django.contrib.auth.models import User
from userauth.models import Interest

class SignupForm(forms.ModelForm):
    confirmation_password = forms.CharField(max_length=16)

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


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['category']