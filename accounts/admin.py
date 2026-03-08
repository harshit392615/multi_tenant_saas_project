from django.contrib import admin
from .models import User , Device
# Register your models here.

@admin.register(User)
class user(admin.ModelAdmin):
    list_display = ['id','username' , 'password' ,"email_verified"]

@admin.register(Device)
class device(admin.ModelAdmin):
    list_display = ['id','user' , 'registration_id' , 'created_at']