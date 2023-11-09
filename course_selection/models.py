from django.db import models

from common.models import Term, StatusChoices, BaseModel
from course.models import Course
from student.models import StudentProfile


class CourseSelectionRequest(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)

    class Meta:
        unique_together = ('student', 'term')


class StudentCourse(BaseModel):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE, related_name="student_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class SubstitutionRequest(BaseModel):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    added_courses = models.ManyToManyField(Course, related_name='substitution_added')
    removed_courses = models.ManyToManyField(Course, related_name='substitution_removed')
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class CourseEmergencyRemovalRequest(BaseModel):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    removed_courses = models.ManyToManyField(Course)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class CourseAppealRequest(BaseModel):
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class TermRemovalRequest(BaseModel):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)
