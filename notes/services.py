from .models import Notes
from common.exceptions import PermissionDenied , ValidationError
from workspace.models import Workspace

def create_note(workspace_slug , actor , organization , serializer):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("you are not allowed to create a note")
    
    workspace = Workspace.objects.get(
        slug = workspace_slug
    )
        
    note = Notes.objects.create(
        organization = organization,
        workspace = workspace,
        **serializer
    )

    return note