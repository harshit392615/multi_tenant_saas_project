from .models import Notes
from workspace.models import Workspace
from common.exceptions import PermissionDenied , ValidationError
from .serializers import notes_Serializer
from enum import Enum

# class UserRole(Enum):


def get_notes(workspace_slug , actor , organization):
    workspace = Workspace.objects.get(slug = workspace_slug)
    if actor.role not in ['owner','admin','member','viewer']:
        raise PermissionDenied("you are not allowed to perform this action")
    notes = Notes.objects.filter(
        workspace = workspace,
        organization = organization
    )

    return notes

def get_note(note_id , membership):
    if not membership:
        raise PermissionDenied("you are not allowed to perform this action")
    content = Notes.objects.values_list(
        "content" , flat=True
    ).get(id = note_id)

    return content
