from django.urls import path
from .views import LoginAPI , RefreshTokenAPI , SignupAPI

urlpatterns = [
    path('login' , LoginAPI.as_view() , name = 'login'),
    path('refresh', RefreshTokenAPI.as_view() , name = 'refresh'),
    path('signup', SignupAPI.as_view() , name = 'signup')
]