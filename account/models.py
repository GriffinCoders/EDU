import random

from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import College, Field, Term, BaseModel


class GenderChoices(models.TextChoices):
    MALE = '0', 'Male'
    FEMALE = '1', 'Female'


class UserRoleChoices(models.TextChoices):
    Student = '0', 'Student'
    Professor = '1', 'Professor'
    ItManager = '2', 'ItManager'
    EducationalAssistance = '3', 'EducationalAssistance'


class User(AbstractUser, BaseModel):
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles')
    meli_code = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=1, choices=UserRoleChoices.choices)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            while True:
                # Generate a random username of 12 digits
                random_username = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                if not User.objects.filter(username=random_username).exists():
                    self.username = random_username
                    break
        super().save(*args, **kwargs)
