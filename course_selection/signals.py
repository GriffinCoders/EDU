from django.dispatch import Signal, receiver
from reportlab.pdfgen import canvas
from io import BytesIO
from course_selection.models import CourseSelectionRequest, StudentCourse
from professor.tasks import send_email_class_schedule, send_email_exam_schedule

from django.db.models.signals import post_save



course_selection_accepted = Signal()

def class_schedule(student):
    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    student_courses = StudentCourse.objects.filter(registration__student=student)

    for student_course in student_courses:
        course_name = student_course.course.lesson.name
        course_day = student_course.course.get_class_day_display()  
        class_start_time = student_course.course.class_start_time.strftime("%H:%M")
        class_end_time = student_course.course.class_finish_time.strftime("%H:%M")
        course_college = student_course.course.lesson.college.name
        course_professor_first_name = student_course.course.professor.user.first_name
        course_professor_last_name = student_course.course.professor.user.last_name
        course_professor = f"{course_professor_first_name} {course_professor_last_name}"
        course_location = student_course.course.class_location

        p.drawString(100, 800, f"Course: {course_name}")
        p.drawString(100, 780, f"Day: {course_day}")
        p.drawString(100, 760, f"Time: {class_start_time} - {class_end_time}")
        p.drawString(100, 740, f"College: {course_college}")
        p.drawString(100, 720, f"Professor: {course_professor}")
        p.drawString(100, 700, f"Location: {course_location}")

        p.showPage()

    p.save()

    buffer.seek(0)

    return buffer.getvalue()



def exam_schedule(student):
    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    student_courses = StudentCourse.objects.filter(registration__student=student)

    for student_course in student_courses:
        course_name = student_course.course.lesson.name
        course_exam_day = student_course.course.exam_specs
        course_college = student_course.course.lesson.college.name
        course_professor_first_name = student_course.course.professor.user.first_name
        course_professor_last_name = student_course.course.professor.user.last_name
        course_professor = f"{course_professor_first_name} {course_professor_last_name}"
        course_location = student_course.course.class_location

        p.drawString(100, 800, f"Course: {course_name}")
        p.drawString(100, 740, f"College: {course_college}")
        p.drawString(100, 740, f"exam: {course_exam_day}")
        p.drawString(100, 720, f"Professor: {course_professor}")
        p.drawString(100, 700, f"Location: {course_location}")

        p.showPage()

    p.save()

    buffer.seek(0)

    return buffer.getvalue()


@receiver(course_selection_accepted, sender=CourseSelectionRequest)
def course_selection_accepted_handler(sender, **kwargs):

    course_selection_request = kwargs['instance']

    class_schedule_pdf_content = class_schedule(course_selection_request.student)
    send_email_class_schedule.delay(
        "Class Schedule",
        "Your class schedule is attached.",
        "yeganegholiour@gmail.com",
        course_selection_request.student.user.email,
        # fail_silently=False,
        
        attachment=(class_schedule_pdf_content, 'class-schedule.pdf', 'application/pdf'),
    )

    exam_schedule_pdf_content = exam_schedule(course_selection_request.student)
    send_email_exam_schedule.delay(
        "Exam Schedule",
        "Your exam schedule is attached.",
        "yeganegholiour@gmail.com",
        course_selection_request.student.user.email,
        # fail_silently=False,

        attachment=(exam_schedule_pdf_content, 'exam-schedule.pdf', 'application/pdf'),
    )


# This activates the signal when the course_selection_request is saved in the AcceptOrRejectStudentForm view
# It calls the course_selection_accepted_handler handler
post_save.connect(course_selection_accepted_handler, sender=CourseSelectionRequest)