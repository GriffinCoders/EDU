from datetime import timedelta, datetime

from django.db import models
from django.db.models import Q

from common.models import Term, StatusChoices, BaseModel
from course.models import Course
from student.models import StudentProfile


class CourseSelectionStatusChoices(models.TextChoices):
    StudentSubmit = '0', 'StudentSubmit'
    Deleted = '1', 'Deleted'
    Pending = '2', 'Pending'
    Failed = '3', 'Failed'
    ProfessorRejected = '4', 'Professor Rejected'
    ProfessorValid = '5', 'Professor Valid'


class CourseSelectionRequest(BaseModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="course_selections")
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    valid_unit = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=1, choices=CourseSelectionStatusChoices.choices)

    class Meta:
        unique_together = ('student', 'term')

    @staticmethod
    def check_student_valid_years(student: StudentProfile):
        return student.valid_years > CourseSelectionRequest.objects.select_related('term').filter(
            student=student,
            term__include_valid_years=True,
        ).count()

    def get_student_gpa(self):
        return self.student_courses.all().aggregate(total_score=models.Sum('score'))['total_score']

    @staticmethod
    def get_student_last_gpa(student: StudentProfile):
        # pass the last student gpa base on CourseSelectionRequest create_at
        requests = CourseSelectionRequest.objects.filter(student=student).order_by('-created_at')
        return requests.first().get_student_gpa() if requests.exists() else None

    def check_student_pass_the_course_prerequisites(self, course: Course):
        prerequisites = course.lesson.prerequisites.all()
        if prerequisites.exists():
            for prerequisite in prerequisites:
                for course_selection in self.student.course_selections.all():
                    if not course_selection.student_courses.filter(course__lesson=prerequisite, passed=True).exists():
                        return False
        return True

    def check_student_course_requisites(self, course: Course):
        requisites = course.lesson.requisites.all()
        if requisites.exists():
            for requisite in requisites:
                # Check if requisite already not exists in course selection
                if not self.student_courses.filter(course__lesson=requisite).exists():
                    for course_selection in self.student.course_selections.all():
                        if course_selection.student_courses.filter(course__lesson=requisite, passed=True).exists():
                            return True
                    return False
        return True

    def has_time_interference(self, new_course):
        # Add one minute to the start time and create a range of time
        start_time = (datetime.combine(datetime.today(), new_course.class_start_time) + timedelta(minutes=1)).time()
        new_course_time_range = (start_time, new_course.class_finish_time)

        # Check for time interference with other StudentCourses in the same registration
        return StudentCourse.objects.filter(
            Q(course__class_start_time__range=new_course_time_range) |
            Q(course__class_finish_time__range=new_course_time_range),
            registration=self,
            course__class_day=new_course.class_day,
        ).exclude(course=new_course).exists()


class StudentCourse(BaseModel):
    registration = models.ForeignKey(CourseSelectionRequest, on_delete=models.CASCADE, related_name="student_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)

    class Meta:
        unique_together = ('registration', 'course')


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
