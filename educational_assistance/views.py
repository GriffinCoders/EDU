from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from professor.models import ProfessorProfile
from student.models import StudentProfile
from . import serializers
from .models import EducationalAssistanceProfile
from .permissions import IsEducationalAssistance


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAuthenticated, IsEducationalAssistance]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        college_id = EducationalAssistanceProfile.objects.get(user=self.request.user).college_id
        return StudentProfile.objects.filter(college_id=college_id).select_related(
            'user', 'entry_term', 'college', 'field', 'supervisor',
        )


class ProfessorViewSet(StudentViewSet):
    serializer_class = serializers.ProfessorSerializer

    def get_queryset(self):
        college_id = EducationalAssistanceProfile.objects.get(user=self.request.user).college_id
        return ProfessorProfile.objects.filter(college_id=college_id).select_related(
            'user', 'college', 'field',
        )
