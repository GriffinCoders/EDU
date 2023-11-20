from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import College, Term, BaseModel
from professor.models import ProfessorProfile

class CourseDayChoices(models.TextChoices):
    SATURDAY = '0', _('Saturday')
    SUNDAY = '1', _('Sunday')
    MONDAY = '2', _('Monday')
    TUESDAY = '3', _('Tuesday')
    WEDNESDAY = '4', _('Wednesday')
    THURSDAY = '5', _('Thursday')
    FRIDAY = '6', _('Friday')

class LessonTypeChoices(models.TextChoices):
    GENERAL = '0', _('General')
    SPECIALIZED = '1', _('Specialized')
    BASIC = '2', _('Basic')

class Lesson(BaseModel):
    name = models.CharField(_('Name'), max_length=128)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    prerequisites = models.ManyToManyField('Lesson', blank=True, related_name='+')
    requisites = models.ManyToManyField('Lesson', blank=True, related_name='+')
    unit = models.PositiveSmallIntegerField(_('Unit'))
    lesson_type = models.CharField(_('Lesson Type'), max_length=1, choices=LessonTypeChoices.choices)

    def __str__(self):
        return self.name

class Course(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    class_day = models.CharField(_('Class Day'), max_length=1, choices=CourseDayChoices.choices)
    class_start_time = models.TimeField(_('Class Start Time'))
    class_finish_time = models.TimeField(_('Class Finish Time'))
    class_location = models.CharField(_('Class Location'), max_length=255, null=True, blank=True)
    exam_specs = models.CharField(_('Exam Specifications'), max_length=255, null=True, blank=True)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveSmallIntegerField(_('Capacity'))
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return _("{lesson} in day: {class_day} in time: {class_start_time} in term: {term}").format(
            lesson=self.lesson.name, class_day=self.get_class_day_display(),
            class_start_time=str(self.class_start_time), term=self.term.name
        )

    def subtract_capacity(self):
        if self.capacity > 0:
            self.capacity -= 1
            self.save()
            return True
        return False

    def increase_capacity(self):
        self.capacity += 1
        self.save()
