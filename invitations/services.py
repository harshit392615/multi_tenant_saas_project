from .models import Invitation
from common.exceptions import PermissionDenied , ValidationError
from organizations.models import Membership
from django.utils import timezone
from enum import Enum

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"
def invite_user(* , organization , actor , email , role , expires_at ):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value]:
        raise PermissionDenied("you are not allowed to perform this action")

    if Membership.objects.filter(
        organization = organization,
        user__email = email,
    ).exists():
        raise PermissionDenied("user is already a member")
    
    
    invitation , _ = Invitation.objects.update_or_create(
        organization = organization,
        email = email,
        defaults={
            'role' : role,
            'accepted_at' : None,
            'expires_at' : expires_at,
        },
    )

    return invitation

def accept_invite(* , token , user):
    try :
        invitation = Invitation.objects.get(token = token)

    except Invitation.DoesNotExist:
        raise ValidationError('invalid Invitation')
    
    if invitation.is_expired:
        raise ValidationError('Invitation expired')
    
    if invitation.is_accepted:
        return #idempotent

    if invitation.email != user.email:
        raise PermissionDenied('you are not allowed to perform this action')
        
    Membership.objects.get_or_create(
        user = user,
        organization = invitation.organization,
        defaults={'role':invitation.role},
    )

    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=['accepted_at',])

    return 1