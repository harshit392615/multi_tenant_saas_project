from django.db import models
from core.models import TenantBaseModel
from workspace.models import Workspace
from autoslug import AutoSlugField
# Create your models here.

class Board(TenantBaseModel):
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , related_name="boards")
    is_archived = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from = 'name',unique=True)


    class Meta:
        unique_together = ('name' , 'workspace')

    def save(self , *args , **kwargs):
        self.organization = self.workspace.organization
        
        super().save(*args , **kwargs)

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"