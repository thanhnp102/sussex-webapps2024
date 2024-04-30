from django import forms
from django.core.validators import EmailValidator
from register.models import User


class SendPaymentForm(forms.Form):
    recipient = forms.EmailField(label="Recipient Email")
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Amount (in your currency)"
    )

    def __init__(self, *args, **kwargs):
        # Get current_user from kwargs (if provided)
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    # Check if Recipient email is valid (exist and is not the current user)
    def clean_recipient(self):
        recipient = self.cleaned_data.get("recipient")
        validator = EmailValidator()
        validator(recipient)
        try:
            user = User.objects.get(email=recipient)  # Check if recipient exists
        except User.DoesNotExist:
            raise forms.ValidationError("Recipient email not found.")
        if recipient == self.current_user.email:
            raise forms.ValidationError("You cannot send money to yourself.")
        return recipient


class RequestPaymentForm(forms.Form):
    receive_user = forms.EmailField(label="Requested User Email")
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Amount (in your currency)"
    )

    def __init__(self, *args, **kwargs):
        # Get current_user from kwargs (if provided)
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    # Check if Receive user email is valid (exist and is not the current user)
    def clean_receive_user(self):
        receive_user = self.cleaned_data.get("receive_user")
        validator = EmailValidator()
        validator(receive_user)
        try:
            user = User.objects.get(email=receive_user)  # Check if recipient exists
        except User.DoesNotExist:
            raise forms.ValidationError("Requested user email not found.")
        if receive_user == self.current_user.email:
            raise forms.ValidationError("You cannot request money from yourself.")
        return receive_user
