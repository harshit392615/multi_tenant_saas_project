from .models import Activity

def get_org_activity(*,organization,limit = 50):
    return Activity.objects.filter(
        organization = organization,
        is_deleted = False,
    )[:limit]


def get_entity_activity(*,organization,entity_id,limit = 50):
    return Activity.objects.filter(
        organization = organization,
        entity_id = entity_id,
        is_deleted = False
    )[:limit]

