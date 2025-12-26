from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignupSerializer
from rest_framework import status
# Create your views here.

class LoginAPI(TokenObtainPairView):
    pass

class RefreshTokenAPI(TokenRefreshView):
    pass
class SignupAPI(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self , request):
        serializer = UserSignupSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
