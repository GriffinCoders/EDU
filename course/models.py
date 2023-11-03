from django.db import models

from common.models import College, Term, BaseModel
from professor.models import ProfessorProfile


class CourseDayChoices(models.TextChoices):
    Saturday = '0', 'Saturday'
    Sunday = '1', 'Sunday'
    Monday = '2', 'Monday'
    Tuesday = '3', 'Tuesday'
    Wednesday = '4', 'Wednesday'
    Thursday = '5', 'Thursday'
    Friday = '6', 'Friday'


class LessonTypeChoices(models.TextChoices):
    General = '0', 'General'
    Specialized = '1', 'Specialized'
    Basic = '2', 'Basic'


class Lesson(BaseModel):
    name = models.CharField(max_length=128)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    prerequisites = models.ManyToManyField('self')
    requisites = models.ManyToManyField('self')
    unit = models.PositiveSmallIntegerField()
    lesson_type = models.CharField(max_length=1, choices=LessonTypeChoices.choices)


class Course(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    class_day = models.CharField(max_length=1, choices=CourseDayChoices.choices)
    class_start_time = models.CharField(max_length=128)
    class_duration = models.FloatField()
    class_location = models.CharField(max_length=255, null=True, blank=True)
    exam_date = models.CharField(max_length=255, null=True, blank=True)
    exam_site = models.OneToOneField(College, on_delete=models.CASCADE)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveSmallIntegerField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
