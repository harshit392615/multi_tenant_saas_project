from django.urls import path 
from .views import CardListCreateAPI

urlpatterns = [
    path('boards/<uuid:board_id>/cards/', CardListCreateAPI.as_view() , name='cardlist'),
]