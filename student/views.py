from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from course_selection.models import CourseSelectionRequest
from course_selection.serializers import CourseSelectionRequestSerializer
from .models import StudentProfile
from .permissions import IsStudent
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return StudentProfile.objects.filter(user=self.request.user).select_related(
            'user', 'entry_term', 'college', 'field', 'supervisor',
        )


class StudentCourseSelectionViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    serializer_class = CourseSelectionRequestSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    @property
    def student_profile(self):
        return StudentProfile.objects.get(user=self.request.user)

    def get_queryset(self):
        return CourseSelectionRequest.objects.filter(student=self.student_profile).prefetch_related("student_courses")

    def get_serializer_context(self):
        return {"student_obj": self.student_profile}
