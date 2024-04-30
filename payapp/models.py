from django.db import models
from register.models import User


class SendPayment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    currency = models.CharField(max_length=3, default="GBP")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.currency} was sent from {self.sender} to {self.recipient}"


class RequestPayment(models.Model):
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_user")
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive_user")
    request_currency = models.CharField(max_length=3, default="GBP")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="Pending")

    def __str__(self):
        return f"{self.amount} {self.request_currency} was requested from {self.receive_user} by {self.request_user}"
