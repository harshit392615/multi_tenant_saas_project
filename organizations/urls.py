from django.urls import path
from .views import Organization_Create_API , Organization_List_API

urlpatterns = [
    path('create', Organization_Create_API.as_view() , name = 'create'),
    path('list',Organization_List_API.as_view() , name='list')
]