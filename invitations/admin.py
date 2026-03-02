from django.contrib import admin
from .models import Invitation

# Register your models here.

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['id','email','organization','role','is_accepted','is_expired','created_at']
    list_filter = ['organization','role','created_at']
    search_fields = ['email']