from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

# Create your views here.

class LoginAPI(TokenObtainPairView):
    pass

class RefreshTokenAPI(TokenRefreshView):
    pass
