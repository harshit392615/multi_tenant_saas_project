from .models import Membership , Organization

def get_org_for_user(*,user):
    organization = Organization.objects.filter(
        membership__user = user,
        is_deleted = False,
        is_archived = False
    )
    return organization