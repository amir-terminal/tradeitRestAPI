from django.db import models
import uuid as uuid_lib
from django.conf import settings
from apps.account.models import User

# Create your models here.


class Message(models.Model):

    message = models.TextField(max_length=200)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        on_delete=models.CASCADE,
        # default=User.objects.get(username='tradeit_user').pk
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver',
        on_delete=models.CASCADE,)

    def __str__(self):
        return self.message
