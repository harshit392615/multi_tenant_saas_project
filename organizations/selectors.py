from .models import Membership , Organization
from common.exceptions import ValidationError

def get_org_for_user(*,user):
    organization = Organization.objects.filter(
        membership__user = user,
        is_deleted = False,
        is_archived = False
    )
    return organization

def get_memebrship_for_org(actor , organization):
    if actor.role not in ['owner','admin','member','viewer']:
        raise ValidationError("you cannot make this request")
    
    memberships = Membership.objects.filter(
        organization = organization
    )
    return memberships