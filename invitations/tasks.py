from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind = True , autoretry_for = {Exception,} , retry_kwargs = {'max_retries:3'})
def send_invitation_email(self,email,org_slug,token):
    invite_url = f'https://{org_slug}.mtsp.com/invite/{token}'
    subject = "You're invited!"
    message = f"Hello,\n\nYou have been invited to join {org_slug}.\nUse this link to accept the invitation:\n{invite_url}\n\nThanks!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )