from django.db import models
from django.utils import timezone
from core.models import TenantBaseModel
import uuid
# Create your models here.

class Invitation(TenantBaseModel):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4 , unique=True)
    accepted_at = models.DateTimeField(null=True ,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
        ('admin','Admin'),
        ('member','Member'),
        ('viewer','Viewer'),
        ]
    )

    class Meta:
        unique_together = ('organization','email')

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    @property
    def is_accepted(self):
        return self.accepted_at is not None
    