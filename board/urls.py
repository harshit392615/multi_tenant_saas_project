from django.urls import path
from .views import BoardListCreateAPI , Board_Delete_API

urlpatterns = [
    path('workspaces/<str:workspace_slug>/boards/' , BoardListCreateAPI.as_view() , name='board_list'),
    path('delete/<int:board_id>',Board_Delete_API.as_view() , name='delete'),
]