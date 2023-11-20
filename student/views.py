from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response

from common.models import StatusChoices
from course_selection.models import CourseSelectionRequest, StudentCourse, CourseSelectionStatusChoices
from course_selection.serializers import CourseSelectionRequestSerializer, CourseSelectionSerializer, \
    check_term_course_selection_time
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
            return Response({"msg": _("Can't delete course that is requisite of other course"
                                    " in this course selection")}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            student_course.course.increase_capacity()
            return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.get_course_selection_object()
        return super().create(request, *args, **kwargs)

    @action(detail=False)
    def submit_courses(self, request, *args, **kwargs):
        course_selection = self.get_course_selection_object()

        # Check status of course selection
        if not course_selection.status == StatusChoices.Pending:
            return Response({"msg": _("Course selection not in pending")}, status=status.HTTP_400_BAD_REQUEST)

        # Check the selection time
        try:
            check_term_course_selection_time(course_selection.term)
        except serializers.ValidationError as e:
            return Response({"msg": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        # Change the course selection pending
        course_selection.status = CourseSelectionStatusChoices.StudentSubmit
        course_selection.save()
        return Response({"msg": _("Course selection submitted")}, status=status.HTTP_200_OK)
