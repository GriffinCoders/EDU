from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return StudentProfile.objects.filter(user=self.request.user).select_related(
            'user', 'entry_term', 'college', 'field', 'supervisor',
        )
