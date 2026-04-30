"""Custom signup form for Record Shelf.

Extends Django's built-in UserCreationForm so we can also collect an email
address at sign-up time.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="We'll only use this to recover your account.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
