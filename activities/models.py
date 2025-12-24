from django.db import models
from core.models import TenantBaseModel
from accounts.models import User
# Create your models here.

class Activity(TenantBaseModel):
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL , null=True , related_name="actor"
    )
    action = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict , blank=True)

    class Meta:
        ordering = ['-created_at']