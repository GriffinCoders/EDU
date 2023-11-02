from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import College, Field, Term


class GenderChoices(models.TextChoices):
    MALE = '0', 'Male'
    FEMALE = '1', 'Female'


class UserRoleChoices(models.TextChoices):
    Student = '0', 'Student'
    Professor = '1', 'Professor'
    ItManager = '2', 'ItManager'
    EducationalAssistance = '3', 'EducationalAssistance'


class User(AbstractUser):
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles')
    meli_code = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=1, choices=UserRoleChoices.choices)
