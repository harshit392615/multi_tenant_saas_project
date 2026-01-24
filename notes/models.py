from django.db import models
from core.models import TenantBaseModel
from accounts.models import User
from workspace.models import Workspace
from autoslug import AutoSlugField
# Create your models here.

class Notes(TenantBaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null=True )
    slug = AutoSlugField(populate_from = 'title',unique=True)
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , null= True )