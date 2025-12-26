from django.urls import path
from .views import LoginAPI , RefreshTokenAPI

urlpatterns = [
    path('login' , LoginAPI.as_view() , name = 'login'),
    path('refresh', RefreshTokenAPI.as_view() , name = 'refresh'),
]