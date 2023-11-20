from io import BytesIO

from reportlab.pdfgen import canvas

from course_selection.models import StudentCourse


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
