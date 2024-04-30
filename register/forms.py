from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from register.models import User
from conversion.currency import get_list


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=sorted(get_list()), initial="GBP")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "currency", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField()  # for email validation
