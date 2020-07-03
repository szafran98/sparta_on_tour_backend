from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class Event(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    can_be_joined_to = models.DateTimeField()
    image_link = models.TextField()

    class Meta:
        ordering = ['-date']

    def normalized_event_date(self):
        return self.date.strftime("%Y.%m.%d %H:%M:%S")

    def normalized_join_date(self):
        return self.can_be_joined_to.strftime("%Y.%m.%d %H:%M:%S")


class Participant(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pesel = models.IntegerField(validators=[MaxValueValidator(99999999999)])
    join_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    joined_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

