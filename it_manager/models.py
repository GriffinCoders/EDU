from django.db import models

from account.models import User
from common.models import BaseModel


class ItManagerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
