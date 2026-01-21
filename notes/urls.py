from django.urls import path
from .views import Notes_List_create

urlpatterns = [
    path('workspaces/<str:workspace_slug>/notes/' , Notes_List_create.as_view() , name='notes')
]