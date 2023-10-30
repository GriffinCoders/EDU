from django.db import models
from django.contrib.auth.models import AbstractUser


class GenderChoices(models.TextChoices):
    MALE = '0', 'Male'
    FEMALE = '1', 'Female'


class GradeChoices(models.TextChoices):
    Associate = '0', 'Associate'
    Undergraduate = '1', 'Undergraduate'
    Postgraduate = '2', 'Postgraduate'
    Doctoral = '3', 'Doctoral'
    Postdoctoral = '4', 'Postdoctoral'


class UserRoleChoices(models.TextChoices):
    Student = '0', 'Student'
    Professor = '1', 'Professor'
    ItManager = '2', 'ItManager'
    EducationalAssistance = '3', 'EducationalAssistance'


class Term(models.Model):
    pass


class College(models.Model):
    pass


class Field(models.Model):
    pass


class User(AbstractUser):
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles')
    meli_code = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=1, null=True)
    birth_date = models.DateField(null=True)
    role = models.CharField(max_length=1, choices=UserRoleChoices.choices)


class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    orientation = models.CharField(max_length=128, null=True)
    order = models.CharField(max_length=128, null=True)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entry_year = models.PositiveSmallIntegerField(null=True)
    entry_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    military_status = models.CharField(max_length=128, null=True, blank=True)
    valid_years = models.PositiveSmallIntegerField(default=10)
    supervisor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=1, choices=GradeChoices.choices)


class ItManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EducationalAssistanceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
