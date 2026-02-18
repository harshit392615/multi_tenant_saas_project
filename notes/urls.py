from django.urls import path
from .views import Notes_List_create ,  Note_Delete_API

urlpatterns = [
    path('workspaces/<str:workspace_slug>/notes/' , Notes_List_create.as_view() , name='notes'),
    path('delete/<int:board_id>',Note_Delete_API.as_view() , name='delete'),
]