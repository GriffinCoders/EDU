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
    name = models.CharField(max_length=128)
    students = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='terms')
    professors = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE)
    courses_list = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='terms')
    selection_start = models.DateTimeField()
    selection_finish = models.DateTimeField()
    class_start = models.DateTimeField()
    class_finish = models.DateTimeField()
    substitution_start = models.DateTimeField()
    substitution_finish = models.DateTimeField()
    emergency_removal_finish = models.DateTimeField()
    exams_start = models.DateTimeField()
    term_finish = models.DateTimeField()


class College(models.Model):
    name = models.CharField(max_length=128)


class Field(models.Model):
    name = models.CharField(max_length=128)
    educational_group = models.CharField(max_length=128)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    units = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=1)


class User(AbstractUser):
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles')
    meli_code = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
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


class Lesson(models.Model):
    name = models.CharField(max_length=128)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    prerequisites = models.ManyToManyField('self') # Ask hasan
    requisites = models.ManyToManyField('self') # Ask hasan
    unit = models.PositiveSmallIntegerField()
    lesson_type = models.CharField(max_length=1, choices=LessonType.choices)


class Course(models.Model):
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


class Course_Per_Student(models.Model):
    registeration = models.ForeignKey(CourseSelection, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=CourseStatusChoices.choices)
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)


class CourseSelection(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)

    class Meta:
        unique_together = ('student', 'term')    

class Registeration_Request(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    request_situation = models.CharField()
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Restoration_Request(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    adding_courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    removing_courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    request_situation = models.CharField()
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Review_Request(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    request_text = models.models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Emergency_Rmoval_Request(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    request_result = models.TextField()
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Term_Removal_Request(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    term = models.OneToOneField(Term, on_delete=models.CASCADE)
    request_result = models.TextField()
    student_explanation = models.TextField()
    educational_assistant_explanation = models.TextField()
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class Employment_Application(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    employment_application_file = models.TextField()
    term = models.OneToOneField(Term, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
