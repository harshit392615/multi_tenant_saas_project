from .models import Workspace
from common.exceptions import PermissionDenied

def Create_Workspace(*,organization , actor , name):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot create a workspace")

    return Workspace.objects.create(
        organization = organization,
        name = name,
    )

def Archive_Workspace(*,workspace,name):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You cannot archive a workspace")
    workspace.is_archived = True
    workspace.save(update_fields = ['is_archived'])
