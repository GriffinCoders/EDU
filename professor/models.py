from django.db import models

from account.models import User
from common.models import College, Field, BaseModel


class ProfessorProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    orientation = models.CharField(max_length=128, null=True)
    order = models.CharField(max_length=128, null=True)
