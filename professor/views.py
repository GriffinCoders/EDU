from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView

from course_selection.serializers import StudentCoursesSerializer, CourseSelectionRequestSerializer
from student.models import StudentProfile
from .permissions import IsProfessor
from common.models import Term
from course_selection.models import StudentCourse, CourseSelectionRequest, CourseSelectionStatusChoices
from professor.models import ProfessorProfile
from professor.serializers import ProfessorSerializer, AcceptOrRejectStudentFormSerializer
from django.shortcuts import get_object_or_404

from .tasks import send_email_class_schedule, send_email_exam_schedule
from .pdf_generator import class_schedule, exam_schedule


class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsProfessor]
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
    return professor == student.supervisor.user


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

            if course_selection_request and course_selection_request.student.supervisor.user == self.request.user:
                courses = StudentCourse.objects.filter(
                    registration=course_selection_request, status=CourseSelectionStatusChoices.Pending
                )
                return courses

        return StudentCourse.objects.none()

    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get("pk")

        student = get_object_or_404(StudentProfile, id=student_id)
        professor = get_object_or_404(ProfessorProfile, user=self.request.user)

        if not check_if_the_right_professor(professor, student):
            return Response(
                {"detail": _("You are not the professor of this student")},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().get(request, *args, **kwargs)


class ListStudentsSelectionForms(ListAPIView):
    serializer_class = CourseSelectionRequestSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        current_term = get_current_term()

        students = StudentProfile.objects.filter(supervisor__user=self.request.user)
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

        if not check_if_the_right_professor(self.request.user, get_object_or_404(StudentProfile, id=student_id)):
            return Response(
                {"detail": _("You are not the professor of this student")},
                status=status.HTTP_403_FORBIDDEN,
            )

        if current_term:
            course_selection_request = get_object_or_404(
                CourseSelectionRequest, student=student_id, term=current_term
            )

            if course_selection_request.status in (CourseSelectionStatusChoices.Pending,
                                                   CourseSelectionStatusChoices.ProfessorRejected):
                return StudentCourse.objects.filter(
                    registration=course_selection_request, status=CourseSelectionStatusChoices.Pending
                )

        return StudentCourse.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = self.kwargs.get("pk")
        current_term = get_current_term()

        try:
            course_selection_request = get_object_or_404(
                CourseSelectionRequest, student=student_id, term=current_term
            )

            if course_selection_request.status in (CourseSelectionStatusChoices.Pending,
                                                   CourseSelectionStatusChoices.ProfessorRejected):
                is_accepted = serializer.validated_data["is_accepted"]

                if is_accepted:
                    course_selection_request.status = CourseSelectionStatusChoices.ProfessorValid
                    course_selection_request.save()

                    student_courses = self.get_queryset()

                    for course in student_courses:
                        course.status = CourseSelectionStatusChoices.ProfessorValid
                        course.save()

                    class_schedule_pdf = class_schedule(get_object_or_404(StudentProfile, id=student_id))
                    exam_schedule_pdf = exam_schedule(get_object_or_404(StudentProfile, id=student_id))
                    student_email = get_object_or_404(User, student=student_id).email

                    send_email_class_schedule.delay(
                        _("Class Schedule"),
                        _("Your class schedule is attached."),
                        "edu.project.bootcamp@gmail.com",
                        student_email,
                        attachment=("Class_Schedule.pdf", class_schedule_pdf, "application/pdf"),
                    )

                    send_email_exam_schedule.delay(
                        _("Exam Schedule"),
                        _("Your exam schedule is attached."),
                        "edu.project.bootcamp@gmail.com",
                        student_email,
                        attachment=("Exam_Schedule.pdf", exam_schedule_pdf, "application/pdf"),
                    )

                    return Response(
                        {"detail": _("Course Selection Was Accepted")},
                        status=status.HTTP_200_OK,
                    )
                else:
                    course_selection_request.status = CourseSelectionStatusChoices.ProfessorRejected
                    course_selection_request.save()
                    return Response(
                        {"detail": _("Course Selection Was Rejected")},
                        status=status.HTTP_200_OK,
                    )

            return Response(
                {"detail": _("Invalid student ID or no pending courses for the current term")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CourseSelectionRequest.DoesNotExist:
            return Response(
                {"detail": _("No course selection request found for the current term")},
                status=status.HTTP_400_BAD_REQUEST,
            )
