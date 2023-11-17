from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response

from course_selection.models import CourseSelectionRequest, StudentCourse
from course_selection.serializers import CourseSelectionRequestSerializer, CourseSelectionSerializer
from .models import StudentProfile
from .permissions import IsStudent
from .serializers import StudentSerializer
from .throtteling import StudentRateThrottle


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    throttle_classes = [StudentRateThrottle]

    def get_queryset(self):
        return StudentProfile.objects.filter(user=self.request.user).select_related(
            'user', 'entry_term', 'college', 'field', 'supervisor',
        )


class StudentCourseSelectionRegistrationViewSet(mixins.CreateModelMixin,
                                                mixins.ListModelMixin,
                                                mixins.RetrieveModelMixin,
                                                viewsets.GenericViewSet):
    serializer_class = CourseSelectionRequestSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    throttle_classes = [StudentRateThrottle]

    @property
    def student_profile(self):
        return StudentProfile.objects.get(user=self.request.user)

    def get_queryset(self):
        return (CourseSelectionRequest.objects.filter(student=self.student_profile)
                .prefetch_related("student_courses").order_by('-created_at'))

    def get_serializer_context(self):
        return {"student_obj": self.student_profile, "request": self.request}


class StudentCourseSelectionViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    serializer_class = CourseSelectionSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    throttle_classes = [StudentRateThrottle]

    def get_course_selection_object(self):
        return get_object_or_404(CourseSelectionRequest, pk=self.kwargs['course_selection_pk'],
                                 student=StudentProfile.objects.get(user=self.request.user))

    def get_queryset(self):
        course_selection = self.get_course_selection_object()
        return StudentCourse.objects.filter(registration=course_selection).order_by('-created_at')

    def get_serializer_context(self):
        return {"course_selection_pk": self.kwargs['course_selection_pk']}

    def destroy(self, request, *args, **kwargs):
        # Check course requisites
        student_course: StudentCourse = self.get_object()
        if student_course.registration.student_courses.filter(
                course__lesson__requisites=student_course.course.lesson
        ).exists():
            return Response({"msg": "Can't delete course that is requisite of other course"
                                    " in this course selection"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            student_course.course.increase_capacity()
            return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.get_course_selection_object()
        return super().create(request, *args, **kwargs)
