from rest_framework.permissions import IsAuthenticated

from professor.models import ProfessorProfile
from professor.serializers import ProfessorSerializer
from professor.views import ProfessorViewSet
from student.models import StudentProfile
from student.views import StudentViewSet
from .models import EducationalAssistanceProfile
from .permissions import IsEducationalAssistance


class AssistanceStudentViewSet(StudentViewSet):
    permission_classes = [IsAuthenticated, IsEducationalAssistance]

    def get_queryset(self):
        college_id = EducationalAssistanceProfile.objects.get(user=self.request.user).college_id
        return StudentProfile.objects.filter(college_id=college_id).select_related(
            'user', 'entry_term', 'college', 'field', 'supervisor',
        )


class AssistanceProfessorViewSet(ProfessorViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsEducationalAssistance]

    def get_queryset(self):
        college_id = EducationalAssistanceProfile.objects.get(user=self.request.user).college_id
        return ProfessorProfile.objects.filter(college_id=college_id).select_related(
            'user', 'college', 'field',
        )

