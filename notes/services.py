from enum import Enum

from .models import Notes
from common.exceptions import PermissionDenied , ValidationError
from workspace.models import Workspace

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

def create_note(workspace_slug , actor , organization , serializer):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value]:
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

def update_note(note_id, ops):
    content = ""

    for op in ops:
        pos = int(op["pos"])

        if op["type"] == "insert":
            content = content[:pos] + op["content"] + content[pos:]

        elif op["type"] == "delete":
            length = int(op["length"])
            content = content[:pos] + content[pos + length:]

    note = Notes.objects.get(id=note_id)
    note.content = content
    note.save()

def Delete_Note(*,id,actor):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value]:
        raise PermissionDenied("you are not allowed to perform this action")
    
    try:
        note = Notes.objects.get(
            id = id 
        )
    except Notes.DoesNotExist: 
        raise ValidationError("invalid organization id")
    
    note.is_deleted =  True

    note.save(update_fields=['is_deleted'])
    return 1