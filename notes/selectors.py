from .models import Notes
from workspace.models import Workspace
from common.exceptions import PermissionDenied , ValidationError

def get_notes(workspace_slug , actor , organization):
    workspace = Workspace.objects.get(slug = workspace_slug)
    if actor.role not in ['owner','admin','member','viewer']:
        raise PermissionDenied("you are not allowed to perform this action")
    notes = Notes.objects.filter(
        workspace = workspace,
        organization = organization
    )

    return notes