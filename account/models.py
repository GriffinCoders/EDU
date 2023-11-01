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


class StatusChoices(models.TextChoices):
    Valid = '0', 'Valid'
    Deleted = '1', 'Deleted'
    Pending = '2', 'Pending'
    Failed = '3', 'Failed'


class CourseDayChoices(models.TextChoices):
    Saturday = '0', 'Saturday'
    Sunday = '1', 'Sunday'
    Monday = '2', 'Monday'
    Tuesday = '3', 'Tuesday'
    Wednesday = '4', 'Wednesday'
    Thursday = '5', 'Thursday'
    Friday = '6', 'Friday'


class LessonType(models.TextChoices):
    General = '0', 'General'
    Specialized = '1', 'Specialized'
    Basic = '2', 'Basic'


class Term(models.Model):
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
    prerequisites = models.ManyToManyField('self')
    requisites = models.ManyToManyField('self')
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


class CourseSelectionRequest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)

    class Meta:
        unique_together = ('student', 'term')


class StudentCourse(models.Model):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class SubstitutionRequest(models.Model):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    added_courses = models.ManyToManyField(Course, related_name='substitution_added')
    removed_courses = models.ManyToManyField(Course, related_name='substitution_removed')
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class CourseEmergencyRemovalRequest(models.Model):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    removed_courses = models.ManyToManyField(Course)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class CourseReviewRequest(models.Model):
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class TermRemovalRequest(models.Model):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)


class StudentRequests(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    request_text = models.TextField()
    response_text = models.TextField()
    status = models.CharField(max_length=1, choices=StatusChoices.choices)
