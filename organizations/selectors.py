from .models import Membership , Organization , Subscription
from common.exceptions import ValidationError
from enum import Enum

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

def get_org_for_user(*,user):
    organization = Organization.objects.filter(
        membership__user = user,
        is_deleted = False,
        is_archived = False
    )
    return organization

def get_memebrship_for_org(actor , organization):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value , UserRole.VIEWER.value]:
        raise ValidationError("you cannot make this request")
    
    memberships = Membership.objects.filter(
        organization = organization
    )
    return memberships

def get_org_subscription(actor , organization):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value , UserRole.VIEWER.value]:
        raise ValidationError("you cannot make this request")
    
    try:
        subscription = Subscription.objects.get(    
        organization = organization)
    except Subscription.DoesNotExist:
        return {
            "title": "free",
            "price": 0,
            "rate_limit": "10/hour",
            "duration": "unlimited",
            "is_active": True
        }
    return subscription

def get_active_users(user , organization):
    memberships = Membership.objects.filter(
        organization = organization
    )