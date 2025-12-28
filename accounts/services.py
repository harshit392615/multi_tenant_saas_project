from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode ,  urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str

from .models import User
from common.exceptions import ValidationError

def send_verification(*,user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return uid , token 
    

def Email_verifier(* , uidb64 , token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except (User.DoesNotExist , ValueError , TypeError):
        raise ValidationError("invalid request")

    if user and default_token_generator.check_token(user , token):
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        return user
    