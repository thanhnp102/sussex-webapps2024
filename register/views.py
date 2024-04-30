from django.shortcuts import render, redirect
from register.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from conversion.currency import convert_currency


def register_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                currency = form.cleaned_data.get("currency")
                if currency == "GBP":
                    user.balance = 1000
                else:
                    exchange = convert_currency("GBP")
                    rate = exchange[currency]
                    user.balance = 1000*rate
                user.save()
                messages.info(request, "User created successfully.")
                login(request, user)
                return redirect("home_login")
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
                return render(request, 'register/register.html', {'register_user': form})
        else:
            form = RegisterForm()
            return render(request, 'register/register.html', {'register_user': form})
    else:
        return redirect("home_login")


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in successfully.")
                    return redirect("home_login")
                else:
                    messages.error(request, "Invalid username or password.")
                    return redirect("login")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("login")
        else:
            form = AuthenticationForm()
            return render(request, "register/login.html", {"login_user": form})
    else:
        return redirect("home_login")


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")
