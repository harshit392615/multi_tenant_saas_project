from django.db import models
from core.models import TenantBaseModel
from workspace.models import Workspace
# Create your models here.

class Board(TenantBaseModel):
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , related_name="boards")
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name' , 'workspace')

    def save(self , *args , **kwargs):
        self.organization = self.workspace.organization
        
        super().save(*args , **kwargs)

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"