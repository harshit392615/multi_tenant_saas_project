from django.urls import path
from .views import BoardListCreateAPI

urlpatterns = [
    path('workspaces/<uuid:workspace_id>/boards/' , BoardListCreateAPI.as_view() , name='board_list')
]