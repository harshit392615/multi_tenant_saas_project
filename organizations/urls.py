from django.urls import path
from .views import Organization_Create_API , Organization_List_API , Organization_Update_API , Organization_Delete_API , Organization_Archive_API

urlpatterns = [
    path('create', Organization_Create_API.as_view() , name = 'create'),
    path('list',Organization_List_API.as_view() , name='list'),
    path('update',Organization_Update_API.as_view() , name='update'),
    path('delete/<uuid:org_id>',Organization_Delete_API.as_view() , name='delete'),
    path('archive',Organization_Archive_API.as_view() , name='archive'),
]