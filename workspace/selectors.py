from enum import Enum

from common.exceptions import PermissionDenied

from .models import Workspace
from django.core.cache import cache

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

def get_workspace_for_org(*,actor,organization):
    if actor.role not in [UserRole.OWNER.value , UserRole.ADMIN.value , UserRole.MEMBER.value , UserRole.VIEWER.value]:
        print(actor.role)
        raise PermissionDenied("you are not allowed to perform this action")
    key = f'org:{organization.id}:workspaces'

    cached = cache.get(key)
    if cached:
        return cached

    qs =  Workspace.objects.filter(
        organization = organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')

    cache.set(key , qs , timeout = 300)
    return qs

def get_workspace_by_slug(*,actor,workspace_slug,organization):
    if actor.role not in [UserRole.OWNER , UserRole.ADMIN , UserRole.MEMBER , UserRole.VIEWER]:
        raise PermissionDenied("you are not allowed to perform this action")

    key = f'org:{organization.id}:workspace_slug:{workspace_slug}'

    cached = cache.get(key)
    if cached:
        return cached

    try:
        workspace = Workspace.objects.filter(
            organization = organization,
            slug = workspace_slug,
            is_archived = False,
            is_deleted = False,
        ).first()
    except Exception as e:
        raise e

    cache.set(key , workspace , timeout = 300)
    return workspace