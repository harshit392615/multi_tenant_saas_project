from .models import Workspace

def get_workspace_for_org(*,organization):
    return Workspace.objects.filter(
        organization = organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')