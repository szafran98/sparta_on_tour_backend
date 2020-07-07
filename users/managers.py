from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have a email')
        if not password:
            raise ValueError('user must have a password')

        user = self.model(email, **extra_fields)
        user.set_password(password)
        user.save()
        return user