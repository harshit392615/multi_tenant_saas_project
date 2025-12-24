from django.db import models
import uuid
# Create your models here.

class Organization(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    ROLE_CHOICES = [
        ('owner','Owner'),
        ('admin','Admin'),
        ('member','Member'),
        ('viewer','Viewer'),
    ]
    user = models.ForeignKey('accounts.User' , on_delete=models.CASCADE , related_name='membership')
    organization = models.ForeignKey(Organization , on_delete= models.CASCADE , related_name='membership')
    role = models.CharField(max_length=20 , choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user' , 'organization')


