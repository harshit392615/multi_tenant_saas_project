from celery import shared_task
from django.core.mail import send_mail 
from dotenv import load_dotenv
import os
load_dotenv()

@shared_task(bind = True , autoretry_for={Exception,} , retry_kwargs = {'max_retries' : 3} )
def send_verification_email(self,*,email,verify_url):
    send_mail(
        subject = 'verify your email',
        message=f'click this link to verify your email,{verify_url}',
        from_email = os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
        fail_silently=False
    )