from django.urls import path
from workspace.views import WorkspaceListCreateAPI , Workspace_Delete_API , WorkspaceDetailsAPI


urlpatterns = [
    path('',WorkspaceListCreateAPI.as_view(),name='workspace-list'),
    path('details/<str:workspace_slug>/',WorkspaceDetailsAPI.as_view(),name='workspace-details'),
    path('delete/<int:workspace_id>/' , Workspace_Delete_API.as_view() , name = "workspace-delete"),
]