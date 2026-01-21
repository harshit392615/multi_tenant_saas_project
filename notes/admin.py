from django.contrib import admin
from .models import Notes
# Register your models here.

@admin.register(Notes)
class notes_admin(admin.ModelAdmin):
    list_display = ["id" , 'title' , 'workspace']