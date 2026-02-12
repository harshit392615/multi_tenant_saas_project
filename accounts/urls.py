from django.urls import path
from .views import LoginAPI , RefreshTokenAPI , SignupAPI , EmailVerifyAPI , Get_User_Activity

app_name = 'accounts'
urlpatterns = [
    path('login/' , LoginAPI.as_view() , name = 'login'),
    path('refresh/', RefreshTokenAPI.as_view() , name = 'refresh'),
    path('signup/', SignupAPI.as_view() , name = 'signup'),
    path('verify/<uidb64>/<token>', EmailVerifyAPI.as_view() , name = 'Email_verify'),
    path('activity/status/' , Get_User_Activity )
]