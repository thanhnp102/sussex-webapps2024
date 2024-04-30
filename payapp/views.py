from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.db import transaction, OperationalError
from .forms import SendPaymentForm, RequestPaymentForm
from .models import SendPayment, RequestPayment
from register.models import User
from conversion.currency import convert_currency
from decimal import Decimal
from django.db.models import Q
from thriftserver.timestamp_client import get_timestamp


def home(request):
    if not request.user.is_authenticated:
        return render(request, "webapps2024/home.html")
    else:
        return redirect("home_login")


@never_cache
def home_login(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        transaction_list = SendPayment.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by('-timestamp')
        request_list = RequestPayment.objects.filter(
            Q(status="Pending"),
            Q(request_user=request.user) | Q(receive_user=request.user)
        ).order_by('timestamp')
        return render(request,
                      "webapps2024/home.html",
                      context={
                          "request_list": request_list,
                          "transaction_list": transaction_list[:5]  # only show upto 5 recent transactions
                      })


def payment_transfer(request, sender, recipient, currency, amount):
    amount = Decimal(amount)
    if request.user.is_authenticated:
        if currency != sender.currency:
            send_amount = Decimal(convert_currency(base_currency=sender.currency)[currency]) * amount
        else:
            send_amount = amount

        # Check if sender has enough funds
        if send_amount > sender.balance:
            raise ValueError("Insufficient funds")

        if currency != recipient.currency:
            receive_amount = Decimal(convert_currency(base_currency=recipient.currency)[currency]) * amount
        else:
            receive_amount = amount

        # Update sender and recipient balances
        sender.balance -= send_amount
        recipient.balance += receive_amount
        sender.save()
        recipient.save()

        # Record the money transfer
        t = SendPayment(sender=sender, recipient=recipient, currency=currency, amount=amount, timestamp=get_timestamp())
        t.save()


@csrf_protect
def send_payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user
            form = SendPaymentForm(request.POST, current_user=current_user)
            if form.is_valid():
                recipient_email = form.cleaned_data.get("recipient")
                try:
                    recipient = User.objects.get(email=recipient_email)
                    currency = current_user.currency
                    amount = form.cleaned_data.get("amount")
                    with transaction.atomic():
                        payment_transfer(
                            request=request,
                            sender=current_user,
                            recipient=recipient,
                            currency=currency,
                            amount=amount
                        )
                    messages.info(request, 'Payment transferred successfully.')
                    return redirect('home_login')
                except OperationalError:
                    messages.error(request, f"Transfer operation is not possible now.")
                return redirect("home_login")
            else:
                messages.error(request, 'Unsuccessful transaction. Invalid information.')
                return render(request, 'payapp/send_payment.html', {'form': form})
        else:
            form = SendPaymentForm()
            return render(request, 'payapp/send_payment.html', {'form': form})
    else:
        return redirect('login')


@csrf_protect
def request_payment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user
            form = RequestPaymentForm(request.POST, current_user=current_user)
            if form.is_valid():
                receive_email = form.cleaned_data.get("receive_user")
                receive_user = User.objects.get(email=receive_email)
                amount = form.cleaned_data.get("amount")
                try:
                    with transaction.atomic():
                        t = RequestPayment(
                            request_user=current_user,
                            receive_user=receive_user,
                            request_currency=current_user.currency,
                            amount=amount,
                            timestamp=get_timestamp(),
                            status="Pending"
                        )
                        t.save()
                    messages.info(request, 'Payment requested successfully.')
                    return redirect('home_login')
                except OperationalError:
                    messages.error(request, f"Request is not possible now.")
                return redirect("home_login")
            else:
                messages.error(request, f"Unsuccessful request. Invalid information.")
                return render(request, 'payapp/request_payment.html', {'form': form})
        else:
            form = RequestPaymentForm()
            return render(request, 'payapp/request_payment.html', {'form': form})
    else:
        return redirect('login')


@csrf_protect
def approve_payment(request, request_id):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                approved_request = RequestPayment.objects.get(id=request_id)
                payment_transfer(
                    request=request,
                    sender=approved_request.receive_user,
                    recipient=approved_request.request_user,
                    currency=approved_request.request_currency,
                    amount=approved_request.amount
                )
                approved_request.status = "Completed"
                approved_request.save()
            messages.info(request, 'Payment Approved.')
        except ValueError:
            messages.error(request, 'Payment Approval Failed.')
        return redirect('home_login')
    else:
        return redirect('home')


@csrf_protect
def reject_payment(request, request_id):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                rejected_request = RequestPayment.objects.get(id=request_id)
                rejected_request.status = "Rejected"
                rejected_request.save()
            messages.info(request, 'Payment Rejected.')
        except ValueError:
            messages.error(request, 'Payment Rejection Failed.')
        return redirect('home_login')
    else:
        return redirect('home')


@csrf_protect
def all_transactions(request):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                transaction_list = SendPayment.objects.filter(
                    Q(sender=request.user) | Q(recipient=request.user)
                ).order_by('-timestamp')
        except ValueError:
            messages.error(request, 'Transaction list is not available.')
        return render(request, 'payapp/transactions.html', context={"transaction_list": transaction_list})
    else:
        return redirect('home')


def timestamp(request):
    timestamp = get_timestamp().strftime("%Y-%m-%d %H:%M:%S")
    return render(request, 'webapps2024/timestamp.html', context={"timestamp": timestamp})
