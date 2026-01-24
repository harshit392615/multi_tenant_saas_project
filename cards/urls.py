from django.urls import path 
from .views import CardListCreateAPI , CardUpdateAPI

urlpatterns = [
    path('boards/<str:board_slug>/cards/', CardListCreateAPI.as_view() , name='cardlist'),
    path('boards/<str:card_slug>/update/', CardUpdateAPI.as_view() , name='cardupdate'),
]