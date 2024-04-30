from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    model = User

    # Admin can view all user accounts and balances
    list_display = ["username", "email", "balance", "currency", "is_staff"]


admin.site.register(User, UserAdmin)
