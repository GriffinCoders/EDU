from celery import shared_task
import time
from django.core.mail import EmailMessage


@shared_task(serializer='json', name="send_email_class_schedule")
def send_email_class_schedule(subject, message, sender, receiver, attachment=None):
    email = EmailMessage(subject, message, sender, [receiver])

    if attachment:
        content, filename, content_type = attachment
        email.attach(filename, content, content_type)

    email.send()


@shared_task(serializer='json', name="send_email_exam_schedule")
def send_email_exam_schedule(subject, message, sender, receiver, attachment=None):
    email = EmailMessage(subject, message, sender, [receiver])

    if attachment:
        content, filename, content_type = attachment
        email.attach(filename, content, content_type)

    email.send()
