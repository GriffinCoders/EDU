from django.db import models


class StatusChoices(models.TextChoices):
    Valid = '0', 'Valid'
    Deleted = '1', 'Deleted'
    Pending = '2', 'Pending'
    Failed = '3', 'Failed'
    Rejected = '4', 'Rejected'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Term(BaseModel):
    name = models.CharField(max_length=128)
    selection_start = models.DateTimeField()
    selection_finish = models.DateTimeField()
    class_start = models.DateTimeField()
    class_finish = models.DateTimeField()
    substitution_start = models.DateTimeField()
    substitution_finish = models.DateTimeField()
    emergency_removal_finish = models.DateTimeField()
    exams_start = models.DateTimeField()
    term_finish = models.DateTimeField()


class College(BaseModel):
    name = models.CharField(max_length=128)


class Field(BaseModel):
    name = models.CharField(max_length=128)
    educational_group = models.CharField(max_length=128)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    units = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=1)
