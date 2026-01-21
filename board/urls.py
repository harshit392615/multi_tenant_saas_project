from django.urls import path
from .views import BoardListCreateAPI

urlpatterns = [
    path('workspaces/<str:workspace_slug>/boards/' , BoardListCreateAPI.as_view() , name='board_list')
]