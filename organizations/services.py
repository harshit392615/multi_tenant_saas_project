from .models import Organization , Membership
from common.exceptions import PermissionDenied ,ValidationError 
from accounts.models import User

def Create_Org(*,user,name,type):
    organization = Organization.objects.create(
        name = name,
        type = type,
    )
    membership = Membership.objects.create(
        user = user,
        organization = organization,
        role = 'owner',
    )

    return organization

def Update_Org(*,slug,actor,name):
    if actor.role != "owner":
        raise PermissionDenied("you are not allowed to perform this action")
    try:
        organization = Organization.objects.get(
            slug = slug
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    
    organization.name = name

    organization.save(update_fields=['name'])

    return organization

def Delete_Org(*,id,actor):
    if actor.role != 'owner':
        raise PermissionDenied("you are not allowed to perform this action")
    
    try:
        organization = Organization.objects.get(
            id = id
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    
    organization.is_deleted =  True

    organization.save(update_fields=['is_deleted'])

def Archive_Org(*,slug,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot archive a workspace")
    try:
        organization = Organization.objects.get(
            slug = slug
        )
    except Organization.DoesNotExist:
        raise ValidationError("invalid organization id")
    organization.is_archived = True
    organization.save(update_fields = ['is_archived'])

def Add_Update_Membership(actor , organization , serializer):
    if actor.role not in ['owner','admin']:
        raise PermissionError("you are not allowed to make this request")
    
    if serializer['role'] not in ['admin','member','viewer']:
        raise ValidationError("not a valid role")
    
    user = User.objects.get(
        email = serializer['email']
    )
    membership = Membership.objects.update_or_create(
        organization = organization,
        user = user,
        role = serializer['role']
    )

    return membership