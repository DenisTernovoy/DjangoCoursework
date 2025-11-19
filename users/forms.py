from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from .models import CustomUser
from django import forms
from config.mixins import StyleFormMixin


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "nickname",
            "avatar",
            "phone",
            "country",
            "password1",
            "password2",
        )


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = CustomUser


class CustomUserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "avatar", "nickname", "phone", "country")
