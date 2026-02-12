from django.db import models
import uuid
from autoslug import AutoSlugField
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Organization(models.Model):
    TYPE_CHOICES = [
        ('personal','Personal'),
        ('team','Team'),
    ]
    id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from = 'name',unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20 ,  choices=TYPE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
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


class Subscription(models.Model):
    TITLE = [
        ('basic' , "Basic"),
        ('standard' , "Standard"),
        ("premium" , "Premium")
    ]
    title = models.CharField(choices=TITLE)
    PRICE = [
        (500,500),
        (1000,1000),
        (5000,5000)
    ]
    price = models.IntegerField(choices=PRICE)
    RATE_LIMIT = [
        ("10/hour","10/hour"),
        ("15/hour","15/hour"),
        ("20/hour","20/hour")
    ]
    rate_limit = models.CharField(choices=RATE_LIMIT)
    DURATION = [
        (30,30),
        (60,60),
        (365,365)
    ]
    duration = models.IntegerField(choices=DURATION)
    organization = models.ForeignKey(Organization , on_delete=models.CASCADE , unique=True)
    start_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    txnid = models.CharField()
    
    @property
    def subscription_status(self):
        return self.start_date + timedelta(days=self.duration) > timezone.now() 