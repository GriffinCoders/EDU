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
    prerequisites = models.ManyToManyField('Lesson', blank=True, related_name='+')
    requisites = models.ManyToManyField('Lesson', blank=True, related_name='+')
    unit = models.PositiveSmallIntegerField()
    lesson_type = models.CharField(max_length=1, choices=LessonTypeChoices.choices)

    def __str__(self):
        return self.name


class Course(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    class_day = models.CharField(max_length=1, choices=CourseDayChoices.choices)
    class_start_time = models.TimeField()
    class_finish_time = models.TimeField()
    class_location = models.CharField(max_length=255, null=True, blank=True)
    exam_specs = models.CharField(max_length=255, null=True, blank=True)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveSmallIntegerField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson.name + " in day: " + self.class_day + " in time: " \
            + str(self.class_start_time) + " in term: " + self.term.name
