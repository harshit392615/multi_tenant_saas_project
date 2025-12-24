from .models import Activity

def log_Activity(*,organization,actor,action,entity_type,entity_id,metadata=None):
    Activity.objects.create(
        organization = organization,
        actor = actor.user,
        action = action,
        entity_type = entity_type,
        entity_id = entity_id,
        metadata = metadata or {},
    )