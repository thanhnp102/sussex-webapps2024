from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    def ready(self):
        User = get_user_model()
        try:
            User.objects.create_superuser(username="admin1", email="admin1@gmail.com", password="admin1")
        except IntegrityError:
            pass
