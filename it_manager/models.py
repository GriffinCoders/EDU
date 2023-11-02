from django.db import models

from account.models import User


class ItManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
