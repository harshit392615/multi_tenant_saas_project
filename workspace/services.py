from .models import Workspace
from common.exceptions import PermissionDenied
from django.core import cache

def Create_Workspace(*,organization , actor , name):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot create a workspace")

    workspace = Workspace.objects.create(
        organization = organization,
        name = name,
    )

    cache.delete(f'org:{organization.id}:workspaces')

    return workspace

def Archive_Workspace(*,workspace,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot archive a workspace")
    workspace.is_archived = True
    workspace.save(update_fields = ['is_archived'])
