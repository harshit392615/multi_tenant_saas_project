from django.contrib import admin
from .models import UserNotification
# Register your models here.

@admin.register(UserNotification)
class notification(admin.ModelAdmin):
    list_display = ("title",'description','seen')