from django.utils import timezone
from student.models import StudentProfile
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from .permissions import IsProfessor
from common.models import StatusChoices, Term
from course_selection.models import StudentCourse, CourseSelectionRequest
from professor.models import ProfessorProfile
from professor.serializers import ProfessorSerializer, AcceptOrRejectStudentFormSerializer
from course_selection.serializers import StudentCoursesSerializer, CourseSelectionRequestSerializer
from django.shortcuts import get_object_or_404

class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return ProfessorProfile.objects.filter(user=self.request.user).select_related(
            'user', 'college', 'field',
        )


def get_current_term():
        current_datetime = timezone.now()
        try:
            current_term = Term.objects.get(
                selection_start__lte=current_datetime,
                selection_finish__gte=current_datetime
            )
            return current_term
        except Term.DoesNotExist:
            return None
    
def check_if_the_right_professor(professor, student):
    if professor == student.supervisor:
        return True
    return False

class RetrieveStudentSelectionForm(RetrieveAPIView):
    serializer_class = StudentCoursesSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        student_id = self.kwargs.get("pk")
        current_term = get_current_term()

        if current_term:
            course_selection_request = CourseSelectionRequest.objects.filter(
                student__id=student_id, term=current_term
            ).first()

            if course_selection_request and course_selection_request.student.supervisor == self.request.user:
                courses = StudentCourse.objects.filter(
                    registration=course_selection_request, status=StatusChoices.Pending
                )
                return courses

        return StudentCourse.objects.none()

    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get("pk")

        student = StudentProfile.objects.get(id=student_id)
        professor = get_object_or_404(ProfessorProfile, user=self.request.user)

        if check_if_the_right_professor(professor, student):
            return super().get(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "You are not the professor of this student"},
                status=status.HTTP_403_FORBIDDEN,
            )
            

class ListStudentsSelectionForms(ListAPIView):
    serializer_class = CourseSelectionRequestSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        current_term = get_current_term()

        students = StudentProfile.objects.filter(supervisor=self.request.user)
        if current_term:
            course_selection_request = CourseSelectionRequest.objects.filter(
                student__in=students, term=current_term
            )
            return course_selection_request

        return CourseSelectionRequest.objects.none()


class AcceptOrRejectStudentForm(ListCreateAPIView):
    serializer_class = AcceptOrRejectStudentFormSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        student_id = self.kwargs.get("pk")
        current_term = get_current_term()

        if check_if_the_right_professor(self.request.user, get_object_or_404(StudentProfile, id=student_id)):
            
            if current_term:
                course_selection_request = get_object_or_404(
                    CourseSelectionRequest, student=student_id, term=current_term
                )

                if course_selection_request.status in (StatusChoices.Pending, StatusChoices.Rejected):
                    return StudentCourse.objects.filter(
                        registration=course_selection_request, status=StatusChoices.Pending
                    )
                return StudentCourse.objects.none()
        else:
            return Response(
                {"detail": "You are not the professor of this student"},
                status=status.HTTP_403_FORBIDDEN,
            )
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = self.kwargs.get("pk")
        current_term = get_current_term()

        try:
            course_selection_request = get_object_or_404(
                CourseSelectionRequest, student=student_id, term=current_term
            )

            if course_selection_request.status in (StatusChoices.Pending, StatusChoices.Rejected):
                is_accepted = serializer.validated_data["is_accepted"]

                if is_accepted:
                    course_selection_request.status = StatusChoices.Valid
                    course_selection_request.save()

                    student_courses = self.get_queryset()

                    for course in student_courses:
                        course.status = StatusChoices.Valid
                        course.save()

                    return Response(
                        {"detail": "Course Selection Was Accepted"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    course_selection_request.status = StatusChoices.Rejected
                    course_selection_request.save()
                    return Response(
                        {"detail": "Course Selection Was Rejected"},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"detail": "Invalid student ID or no pending courses for the current term"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CourseSelectionRequest.DoesNotExist:
            return Response(
                {"detail": "No course selection request found for the current term"},
                status=status.HTTP_400_BAD_REQUEST,
            )





