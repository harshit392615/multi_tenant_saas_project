from django.urls import path
from workspace.views import WorkspaceListCreateAPI , Workspace_Delete_API


urlpatterns = [
    path('',WorkspaceListCreateAPI.as_view(),name='workspace-list'),
    path('delete/<int:workspace_id>' , Workspace_Delete_API.as_view() , name = "workspace-delete"),
]