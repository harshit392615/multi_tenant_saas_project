from django.contrib import admin
from .models import Organization , Membership
# Register your models here.

@admin.register(Organization)
class Organization(admin.ModelAdmin):
    list_display = ['name','slug','is_deleted','is_archived' , 'slug']

@admin.register(Membership)

class Membership(admin.ModelAdmin):
    list_display = ["organization" , "user" , 'role']