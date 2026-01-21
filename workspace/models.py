from django.db import models
from core.models import TenantBaseModel
from autoslug import AutoSlugField
# Create your models here.

class Workspace(TenantBaseModel):
    name = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from = 'name' , unique = True, null = True)
    class Meta:
        unique_together = ('name','organization')

    def __str__(self):
        return f"{self.name}({self.organization.slug})"