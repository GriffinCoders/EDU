from django.utils import timezone

from rest_framework import serializers

from common.models import StatusChoices, Term
from common.serializers import CustomChoiceField
from course_selection.models import CourseSelectionRequest, StudentCourse


class StudentCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = [
            "id",
            "course",
            "score",
            "passed",
            "status",
        ]


class CourseSelectionRequestSerializer(serializers.ModelSerializer):
    term_courses = StudentCoursesSerializer(many=True, source="student_courses", read_only=True)
    status = CustomChoiceField(choices=StatusChoices.choices, read_only=True)

    class Meta:
        model = CourseSelectionRequest
        fields = [
            "id",
            "term",
            "status",
            "term_courses",
        ]

    def validate(self, attrs):
        term: Term = attrs.get('term')
        if CourseSelectionRequest.objects.filter(student=self.context['student_obj'], term=term).exists():
            raise serializers.ValidationError("The Course Selection for this term already exists")
        now = timezone.now()
        if term.selection_start > now:
            raise serializers.ValidationError("The Course Selection not started")
        if term.selection_finish < now:
            raise serializers.ValidationError("The Course Selection time has passed")
        return attrs

    def create(self, validated_data):
        validated_data["student"] = self.context['student_obj']
        validated_data["status"] = StatusChoices.Pending
        return super().create(validated_data)
