from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from course_selection.models import CourseSelectionRequest, StudentCourse
from course_selection.serializers import CourseSelectionRequestSerializer, CourseSelectionSerializer
from .models import StudentProfile
from .permissions import IsStudent
from .serializers import StudentSerializer
from .throtteling import StudentRateThrottle

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from tasks import send_email_class_schedule, send_email_exam_schedule


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


def class_schedule(student):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="class-schedule.pdf"'

    student_course = StudentCourse.objects.filter(registration__student=student)

    p = canvas.Canvas(response)

    for student_course in student_course:
        course_name = student_course.course.lesson.name
        course_day = student_course.course.get_class_day_display()  
        class_start_time = student_course.course.class_start_time.strftime("%H:%M")
        class_end_time = student_course.course.class_finish_time.strftime("%H:%M")
        course_college = student_course.course.lesson.college.name
        course_professor = student_course.course.professor.name
        course_location = student_course.course.class_location

        p.drawString(100, 800, f"Course: {course_name}")
        p.drawString(100, 780, f"Day: {course_day}")
        p.drawString(100, 760, f"Time: {class_start_time} - {class_end_time}")
        p.drawString(100, 740, f"College: {course_college}")
        p.drawString(100, 720, f"Professor: {course_professor}")
        p.drawString(100, 700, f"Location: {course_location}")

        p.showPage()

    p.save()

    return response
        

def exam_schedule(student):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exam-schedule.pdf"'

    student_course = StudentCourse.objects.filter(registration__student=student)

    p = canvas.Canvas(response)

    for student_course in student_course:
        course_name = student_course.course.lesson.name
        course_exam_day = student_course.course.exam_specs
        course_college = student_course.course.lesson.college.name
        course_professor = student_course.course.professor.name
        course_location = student_course.course.class_location

        p.drawString(100, 800, f"Course: {course_name}")
        p.drawString(100, 740, f"College: {course_college}")
        p.drawString(100, 740, f"exam: {course_exam_day}")
        p.drawString(100, 720, f"Professor: {course_professor}")
        p.drawString(100, 700, f"Location: {course_location}")

        p.showPage()

    p.save()

    return response


class SendClassScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get(self, request):
        student = request.user
        schedule = class_schedule(student)
        
        try: 
            send_email_class_schedule.delay(
                subject="class-schedule",
                message=schedule.content,
                sender="yeganegholiour@gmail.com",
                receiver="student-gmail"
            )
            
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise e


class SendExamScheduleView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    
    def get(self, request):
        student = request.user
        schedule = exam_schedule(student)
        
        try: 
            send_email_exam_schedule.delay(
                subject="class-schedule",
                message=schedule.content,
                sender="yeganegholiour@gmail.com",
                receiver="student-gmail"
            )
            
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
