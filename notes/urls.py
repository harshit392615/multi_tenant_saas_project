from django.urls import path
from .views import Notes_List_create ,  Note_Delete_API , Note_List_For_Org , Note_Details_API

urlpatterns = [
    path('workspaces/<str:workspace_slug>/notes/' , Notes_List_create.as_view() , name='notes'),
    path('list/' , Note_List_For_Org.as_view() , name='notes_list'),
    path("<int:note_id>/" , Note_Details_API.as_view() , name='notes_details'),
    path('delete/<int:board_id>',Note_Delete_API.as_view() , name='delete'),
]