"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_login, name="home_login"),
    path('send_payment/', views.send_payment, name="send_payment"),
    path('request_payment/', views.request_payment, name="request_payment"),
    path('approve_request/<int:request_id>/', views.approve_payment, name='approve_payment'),
    path('reject_payment/<int:request_id>/', views.reject_payment, name='reject_payment'),
    path('transactions/', views.all_transactions, name="transactions"),
]
