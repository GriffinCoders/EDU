from celery import shared_task
from django.core.mail import EmailMessage

from EDU.settings import EMAIL_HOST_USER


@shared_task
def send_otp_email(otp_code, receiver):
    email = EmailMessage("otp from edu", f"otp-code: {otp_code}", EMAIL_HOST_USER, [receiver])
    email.send()
