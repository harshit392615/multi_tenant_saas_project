from celery import shared_task
from django.core.mail import send_mail 
from dotenv import load_dotenv
from django.conf import settings
import os
load_dotenv()

@shared_task(bind = True , autoretry_for={Exception,} , retry_kwargs = {'max_retries' : 3} )
def send_verification_email(self,*,email,verify_url):
    send_mail(
        subject = 'verify your email',
        message=f'click this link to verify your email,{verify_url}',
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )