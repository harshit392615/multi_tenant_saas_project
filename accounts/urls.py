from django.urls import path
from .views import ForgotPasswordSender, Forgot_Password_Reset_API, LoginAPI , RefreshTokenAPI , SignupAPI , EmailVerifyAPI , Get_User_Activity , Password_Reset_API

app_name = 'accounts'
urlpatterns = [
    path('login/' , LoginAPI.as_view() , name = 'login'),
    path('refresh/', RefreshTokenAPI.as_view() , name = 'refresh'),
    path('signup/', SignupAPI.as_view() , name = 'signup'),
    path('verify/<str:uidb64>/<str:token>/', EmailVerifyAPI.as_view() , name = 'Email_verify'),
    path('activity/status/' , Get_User_Activity ),
    path('forgot-password/' , ForgotPasswordSender.as_view() , name = 'forgot_password'),
    path('forgot-password-reset/' , Forgot_Password_Reset_API.as_view() , name = 'Forgot_reset_password'),
    path('password-reset/' , Password_Reset_API.as_view() , name = 'reset_password'),
]