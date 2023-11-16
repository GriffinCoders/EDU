from rest_framework import serializers
from .models import Lesson, Course

from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from rest_framework import serializers

from common.models import StatusChoices, Term
from course.models import Course
from course_selection.models import CourseSelectionRequest, StudentCourse
from student.models import StudentProfile



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'college', 'prerequisites', 'requisites', 'unit', 'lesson_type']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['lesson', 'class_day', 'class_start_time', 'class_duration', 'class_location', 'exam_date', 'exam_site', 'professor', 'capacity', 'term']


    # validate method to check if substitution time is finished or not
    def validate(self, attrs):
        # check the duplication term for the student
        term: Term = attrs.get('term')
        student: StudentProfile = self.context['student_obj']
        if CourseSelectionRequest.objects.filter(student=student, term=term).exists():
            raise serializers.ValidationError("The Course Selection for this term already exists")

        # Check the selection time
        now = timezone.now()
        if term.substitution_start > now:
            raise serializers.ValidationError("The Course Selection not started")
        if term.substitution_finish < now:
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
         
