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
        # Check the substitution time
        term: Term = attrs.get('term')
        
        now = timezone.now()
        if term.substitution_finish < now and term.term_finish > now:
            raise serializers.ValidationError("The Course Substitution is not possible")

        return attrs
         
