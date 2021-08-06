'''from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, validators=[MinLengthValidator(6)], required=True, widget=forms.TextInput(attrs={
        "autocomplete": "off",
        "placeholder": "Username",
    }))
    password = forms.PasswordInput(widget=forms.TextInput(attrs={
        "autocomplete": "off",
        "placeholder": "Password",
    }))


class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=30, widget={
        "autocomplete": "off",
        "placeholder": "Username",
    })
    password = forms.PasswordInput(label="password", max_length=30, widget={
        "autocomplete": "off",
        "placeholder": "Password",
    })
    confirmation = forms.PasswordInput(label="confirm-password", max_length=30, widget={
        "autocomplete": "off",
        "placeholder": "Confirm Password",
    })
    email = forms.EmailField(label="email", max_length=30, widget={
        "autocomplete": "off",
        "placeholder": "Email",
    })'''

