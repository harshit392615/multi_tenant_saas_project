from .models import Workspace
from django.core.cache import cache

def get_workspace_for_org(*,organization):
    key = f'org:{organization.id}:workspaces'

    cached = cache.get(key)
    if cached:
        return cached
    
    print(cached)

    qs =  Workspace.objects.filter(
        organization = organization,
        is_archived = False,
          # is_deleted = False,
    ).order_by('created_at')

    cache.set(key , qs , timeout = 300)
    return qs