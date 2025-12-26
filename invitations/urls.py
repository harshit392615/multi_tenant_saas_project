from django.urls import path
from .views import Accept_User_API , Invite_User_API

urlpatterns = [
    path('/invite', Invite_User_API.as_view() , name = 'invite'),
    path('/accept', Accept_User_API.as_view() , name = 'accept')
]