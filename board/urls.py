from django.urls import path
from .views import BoardListCreateAPI , Board_Delete_API , Board_List_For_Org , BoardDetailsAPI

urlpatterns = [
    path('workspaces/<str:workspace_slug>/boards/' , BoardListCreateAPI.as_view() , name='board_list'),
    path('list/' , Board_List_For_Org.as_view() , name='notes_list'),
    path('delete/<int:board_id>/',Board_Delete_API.as_view() , name='delete'),
    path('details/<str:board_slug>/',BoardDetailsAPI.as_view() , name='board_details'),
]