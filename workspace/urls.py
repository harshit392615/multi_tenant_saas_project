from django.urls import path
from workspace.views import WorkspaceListCreateAPI


urlpatterns = [
    path('',WorkspaceListCreateAPI.as_view(),name='workspace-list')
]