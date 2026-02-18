from .models import Workspace
from common.exceptions import PermissionDenied
from activities.services import log_Activity
from django.core.cache import cache
from common.exceptions import PermissionDenied ,ValidationError 

def Create_Workspace(*,organization , actor , name):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot create a workspace")

    workspace = Workspace.objects.create(
        organization = organization,
        name = name,
    )

    cache.delete(f'org:{organization.id}:workspaces')

    log_Activity(organization=organization , actor=actor , action="workspace created" , entity_type="workspace" , entity_id=workspace.id ,  )

    return workspace

def Archive_Workspace(*,workspace,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot archive a workspace")
    workspace.is_archived = True
    workspace.save(update_fields = ['is_archived'])

def Delete_Workspace(*,id,actor):
    if actor.role not in  ['owner','admin']:
        raise PermissionDenied("you are not allowed to perform this action")
    
    try:
        workspace = Workspace.objects.get(
            id = id 
        )
    except Workspace.DoesNotExist: 
        raise ValidationError("invalid organization id")
    
    workspace.is_deleted =  True

    workspace.save(update_fields=['is_deleted'])
    return 1