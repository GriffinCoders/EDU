from django.utils import timezone
from rest_framework import serializers

from common.models import Term
from course.models import Course
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'college',
            'prerequisites',
            'requisites',
            'unit',
            'lesson_type',
        ]

    def create(self, validated_data):
        college = self.context.get('college', None)
        if college and not validated_data.get('college') == college:
            raise serializers.ValidationError("Can't create lesson for other colleges")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        college = self.context.get('college', None)
        if college and not validated_data.get('college') == college:
            raise serializers.ValidationError("Can't update lesson for other colleges")
        return super().update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'lesson',
            'class_day',
            'class_start_time',
            'class_finish_time',
            'class_location',
            'exam_specs',
            'professor',
            'capacity',
            'term',
        ]

    def validate(self, attrs):
        # Check the substitution time
        term: Term = attrs.get('term')
        now = timezone.now()
        if term.substitution_finish < now:
            raise serializers.ValidationError("The Course Substitution is passed")
        return attrs

    def create(self, validated_data):
        college = self.context.get('college', None)
        if college and not validated_data.get('lesson').college == college:
            raise serializers.ValidationError("Can't create course that lesson is for other colleges")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        college = self.context.get('college', None)
        if college and not validated_data.get('lesson').college == college:
            raise serializers.ValidationError("Can't update course that lesson is for other colleges")
        return super().update(instance, validated_data)
