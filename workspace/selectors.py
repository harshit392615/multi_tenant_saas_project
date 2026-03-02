from .models import Workspace
from django.core.cache import cache

def get_workspace_for_org(*,organization):
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

def get_workspace_by_slug(*,workspace_slug,organization):
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