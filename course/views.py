# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.models import UserRoleChoices
from educational_assistance.models import EducationalAssistanceProfile
from .models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer
from .permissions import IsEducationalAssistanceOrItManager


def get_lesson_queryset(user):
    if user.role == UserRoleChoices.EducationalAssistance:
        return Lesson.objects.filter(college=EducationalAssistanceProfile.objects.get(user=user).college)
    return Lesson.objects.all()


def get_course_queryset(user):
    if user.role == UserRoleChoices.EducationalAssistance:
        return Course.objects.filter(lesson__college=EducationalAssistanceProfile.objects.get(user=user).college)
    return Course.objects.all()


class LessonListView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return get_lesson_queryset(self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsEducationalAssistanceOrItManager()]

    def get_serializer_context(self):
        if self.request.user.is_authenticated and self.request.user.role == UserRoleChoices.EducationalAssistance:
            return {"college": EducationalAssistanceProfile.objects.get(user=self.request.user).college}
        return {}


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return get_lesson_queryset(self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsEducationalAssistanceOrItManager()]

    def get_serializer_context(self):
        if self.request.user.is_authenticated and self.request.user.role == UserRoleChoices.EducationalAssistance:
            return {"college": EducationalAssistanceProfile.objects.get(user=self.request.user).college}
        return {}


class CourseListView(LessonListView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return get_course_queryset(self.request.user)


class CourseDetailView(LessonDetailView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return get_course_queryset(self.request.user)
