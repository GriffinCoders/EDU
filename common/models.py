from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoices(models.TextChoices):
    Valid = '0', _('Valid')
    Deleted = '1', _('Deleted')
    Pending = '2', _('Pending')
    Failed = '3', _('Failed')
    Rejected = '4', _('Rejected')


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


class Term(BaseModel):
    name = models.CharField(_('Name'), max_length=128)
    selection_start = models.DateTimeField(_('Selection Start'))
    selection_finish = models.DateTimeField(_('Selection Finish'))
    class_start = models.DateTimeField(_('Class Start'))
    class_finish = models.DateTimeField(_('Class Finish'))
    substitution_start = models.DateTimeField(_('Substitution Start'))
    substitution_finish = models.DateTimeField(_('Substitution Finish'))
    emergency_removal_finish = models.DateTimeField(_('Emergency Removal Finish'))
    exams_start = models.DateTimeField(_('Exams Start'))
    term_finish = models.DateTimeField(_('Term Finish'))
    include_valid_years = models.BooleanField(_('Include Valid Years'))

    def __str__(self):
        return self.name


class College(BaseModel):
    name = models.CharField(_('Name'), max_length=128)

    def __str__(self):
        return self.name


class Field(BaseModel):
    name = models.CharField(_('Name'), max_length=128)
    educational_group = models.CharField(_('Educational Group'), max_length=128)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    units = models.PositiveSmallIntegerField(_('Units'))
    grade = models.CharField(_('Grade'), max_length=1)

    def __str__(self):
        return self.name
