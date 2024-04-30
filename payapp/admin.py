from django.contrib import admin
from .models import SendPayment, RequestPayment


# Admin can view all payment transactions and requests history

admin.site.register(SendPayment)
admin.site.register(RequestPayment)
