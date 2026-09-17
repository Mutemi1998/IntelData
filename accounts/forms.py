from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(
                username=username,
                password=password
            )

            if self.user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            if not self.user.is_active:
                raise forms.ValidationError(
                    "This account is disabled."
                )

        return cleaned_data

    def get_user(self):
        return self.user


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    first_name = forms.CharField(
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )
    
    organization_name = forms.CharField(
        max_length=150,
        required=True
    )

    phone = forms.CharField(
        max_length=30,
        required=False
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "organization_name",
            "phone",
            "password1",
            "password2",
        ]