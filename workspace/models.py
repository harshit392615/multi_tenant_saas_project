from django.db import models
from core.models import TenantBaseModel
# Create your models here.

class Workspace(TenantBaseModel):
    name = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name','organization')

    def __str__(self):
        return f"{self.name}({self.organization.slug})"