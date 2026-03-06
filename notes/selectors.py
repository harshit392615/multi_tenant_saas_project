from .models import Notes
from workspace.models import Workspace
from common.exceptions import PermissionDenied , ValidationError
from .serializers import notes_Serializer
from enum import Enum

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


def get_notes(workspace_slug , actor , organization):
    workspace = Workspace.objects.get(slug = workspace_slug)
    if actor is None or actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value , UserRole.VIEWER.value]:
        raise PermissionDenied("you are not allowed to perform this action")
    notes = Notes.objects.filter(
        workspace = workspace,
        organization = organization
    )

    return notes

def get_notes_for_org(actor , organization):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value , UserRole.VIEWER.value]:
        raise PermissionDenied("you are not allowed to perform this action")
    notes = Notes.objects.filter(
        organization = organization
    )

    return notes
def get_note(note_id , actor):
    print(actor)
    if not actor:
        raise PermissionDenied("you are not allowed to perform this action")
    note = Notes.objects.get(
        id = note_id,
    )

    return note
