from django.db import models
from core.models import TenantBaseModel
from accounts.models import User
from workspace.models import Workspace
# Create your models here.

class Notes(TenantBaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , null= True )