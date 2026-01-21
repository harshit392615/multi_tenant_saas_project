from django.db import models

# Create your models here.
class TenantBaseModel(models.Model):
    organization = models.ForeignKey('organizations.Organization' , on_delete=models.CASCADE , related_name="%(class)s_set")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.BooleanField(null = True)
    is_deleted = models.BooleanField(default=False)

    class Meta():
        abstract = True