from django.db import models
from core.models import TenantBaseModel
from board.models import Board , Workspace
from accounts.models import User
from autoslug import AutoSlugField
# Create your models here.

class Card(TenantBaseModel):
    STATUS_CHOICES = (
        ('todo','To Do'),
        ('inprogress','In Progress'),
        ('done','Done'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_archived = models.BooleanField(default=False)
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='todo')
    assignee = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_cards')
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='cards')
    due_date = models.DateTimeField(null=True,blank=True)
    board = models.ForeignKey(Board , on_delete=models.CASCADE )
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , null=True , blank=True)
    slug = AutoSlugField(populate_from = 'title',unique=True)


    def save(self , *args , **kwargs):
        self.organization = self.board.organization

        super().save(*args,**kwargs)

    def __str__(self):
        return self.title

