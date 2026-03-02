from django.urls import path 
from .views import CardDeleteAPI, CardListCreateAPI , CardUpdateAPI , CardListForOrg ,CardListForWorkspace

urlpatterns = [
    path('boards/<str:board_slug>/cards/', CardListCreateAPI.as_view() , name='cardlist'),
    path('list/', CardListForOrg.as_view() , name='cardlist'),
    path('workspace/<str:workspace_slug>/list/', CardListForWorkspace.as_view() , name='cardlist'),
    path('boards/<str:card_slug>/update/', CardUpdateAPI.as_view() , name='cardupdate'),
    path('boards/<int:card_id>/delete/', CardDeleteAPI.as_view() , name='carddelete'),
]