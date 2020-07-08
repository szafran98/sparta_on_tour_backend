from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    pesel = models.CharField(max_length=11)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'pesel']

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.email)

    @staticmethod
    def check_pesel_duplicates(pesel):
        accounts = CustomUser.objects.filter(pesel=pesel)
        if accounts.count() != 0:
            return True