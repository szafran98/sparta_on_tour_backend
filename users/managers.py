from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have a email')
        if not password:
            raise ValueError('user must have a password')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
