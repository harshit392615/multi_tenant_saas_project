from django.db import models
from core.models import TenantBaseModel
from accounts.models import User
from organizations.models import Organization
# Create your models here.

class UserNotification(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='notifications')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)