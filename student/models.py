from django.db import models

from account.models import User
from common.models import Term, College, Field, StatusChoices, BaseModel
from professor.models import ProfessorProfile


class GradeChoices(models.TextChoices):
    Associate = '0', 'Associate'
    Undergraduate = '1', 'Undergraduate'
    Postgraduate = '2', 'Postgraduate'
    Doctoral = '3', 'Doctoral'
    Postdoctoral = '4', 'Postdoctoral'


class StudentProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entry_year = models.PositiveSmallIntegerField(null=True)
    entry_term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    military_status = models.CharField(max_length=128, null=True, blank=True)
    valid_years = models.PositiveSmallIntegerField(default=10)
    supervisor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=1, choices=GradeChoices.choices)


class StudentRequests(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    request_text = models.TextField()
    request_title = models.CharField(max_length=128)
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)
