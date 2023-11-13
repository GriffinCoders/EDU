from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from rest_framework import serializers

from common.models import StatusChoices, Term
from common.serializers import CustomChoiceField
from course.models import Course
from course_selection.models import CourseSelectionRequest, StudentCourse
from student.models import StudentProfile


class StudentCoursesSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=StatusChoices.choices, read_only=True)
    course_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentCourse
        fields = [
            "id",
            "course",
            "course_detail",
            "score",
            "passed",
            "status",
        ]

    @staticmethod
    def get_course_detail(obj):
        return obj.course.__str__()


class CourseSelectionRequestSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=StatusChoices.choices, read_only=True)
    student_term_courses = StudentCoursesSerializer(many=True, source="student_courses", read_only=True)
    courses_path = serializers.SerializerMethodField(read_only=True)
    term_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseSelectionRequest
        fields = [
            "id",
            "term",
            "term_name",
            "status",
            "valid_unit",
            "student_term_courses",
            "courses_path",
        ]
        extra_kwargs = {
            'valid_unit': {'read_only': True},
        }

    @staticmethod
    def get_term_name(obj):
        return obj.term.__str__()

    def get_courses_path(self, obj):
        return self.context['request'].build_absolute_uri(
            reverse('student:courses-list', kwargs={'course_selection_pk': obj.id})
        )

    def validate(self, attrs):
        # check the duplication term for the student
        term: Term = attrs.get('term')
        student: StudentProfile = self.context['student_obj']
        if CourseSelectionRequest.objects.filter(student=student, term=term).exists():
            raise serializers.ValidationError("The Course Selection for this term already exists")

        # Check the selection time
        now = timezone.now()
        if term.selection_start > now:
            raise serializers.ValidationError("The Course Selection not started")
        if term.selection_finish < now:
            raise serializers.ValidationError("The Course Selection time has passed")

        # Check the valid years
        if not CourseSelectionRequest.check_student_valid_years(student):
            raise serializers.ValidationError("Not enough valid years")

        # Check the last term gpa
        attrs['valid_unit'] = 20
        last_gpa = CourseSelectionRequest.get_student_last_gpa(student)
        if last_gpa and last_gpa >= 17:
            attrs['valid_unit'] = 24

        return attrs

    def create(self, validated_data):
        validated_data["student"] = self.context['student_obj']
        validated_data["status"] = StatusChoices.Pending
        return super().create(validated_data)


class CourseSelectionSerializer(serializers.ModelSerializer):
    course_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentCourse
        fields = ["id", "course", "course_detail"]

    @staticmethod
    def get_course_detail(obj):
        return obj.course.__str__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_selection = None

    def validate(self, attrs):
        self.course_selection = CourseSelectionRequest.objects.get(pk=self.context['course_selection_pk'])

        # Check the selection time
        now = timezone.now()
        term: Term = self.course_selection.term
        if term.selection_start > now:
            raise serializers.ValidationError("The Course Selection time not started")
        if term.selection_finish < now:
            raise serializers.ValidationError("The Course Selection time has passed")

        course: Course = attrs.get("course")

        # Check the duplication course
        if StudentCourse.objects.filter(registration=self.course_selection, course=course):
            raise serializers.ValidationError("The user already picked this course in this term")

        # Check the course prerequisites
        if not self.course_selection.check_student_pass_the_course_prerequisites(course):
            raise serializers.ValidationError("Course Prerequisites not passed")

        # Check lesson college
        if not course.lesson.college == self.course_selection.student.college:
            raise serializers.ValidationError("Lesson college does not match student college")

        # Check requisites
        if not self.course_selection.check_student_course_requisites(course):
            raise serializers.ValidationError("Course requisites not picked or passed")

        # Check course capacity
        if not course.capacity > 0:
            raise serializers.ValidationError("Course doesn't have any capacity")

        # Check course time interference
        if self.course_selection.has_time_interference(course):
            raise serializers.ValidationError("Course has time interference")

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            # Create the student course
            validated_data["registration"] = self.course_selection
            validated_data["status"] = StatusChoices.Pending
            obj = super().create(validated_data)

            # subtract course capacity
            if not validated_data['course'].subtract_capacity():
                raise serializers.ValidationError("Course doesn't have any capacity")
        return obj
