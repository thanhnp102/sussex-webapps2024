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
from django.contrib import admin
from django.urls import path, include
import register.views
import payapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', payapp.views.home, name="home"),
    path('home/', payapp.views.home, name="home"),
    path('register/', register.views.register_user, name="register"),
    path('login/', register.views.login_user, name="login"),
    path('logout/', register.views.logout_user, name="logout"),
    path('account/', include("payapp.urls")),
    path('conversion/', include("conversion.urls")),
    path('timestamp/', payapp.views.timestamp, name="timestamp"),
]
