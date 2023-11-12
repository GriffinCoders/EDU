from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from professor.models import ProfessorProfile
from professor.serializers import ProfessorSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return ProfessorProfile.objects.filter(user=self.request.user).select_related(
            'user', 'college', 'field',
        )
