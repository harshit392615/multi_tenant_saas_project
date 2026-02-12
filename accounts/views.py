from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignupSerializer
from rest_framework import status
from .services import send_verification ,Email_verifier
from django.urls import reverse
from .tasks import send_verification_email
from core.auth import authenticate_bearer_by_token
from .selectors import get_status
from django.http import StreamingHttpResponse , HttpResponseForbidden

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
            uid , token = send_verification(user=user)
            verify_url = request.build_absolute_uri(reverse("accounts:Email_verify" , kwargs={"uidb64":uid , "token":token}))
            send_verification_email.delay(email = user.email , verify_url=verify_url)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class EmailVerifyAPI(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self , request , uidb64 , token):
        Email_verifier(uidb64=uidb64 , token=token)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def Get_User_Activity(request):
    token = request.GET.get('token')
    print(token)
    try:
        user = authenticate_bearer_by_token(token)
        print(user)
    except Exception:
        return HttpResponseForbidden("Unauthorized")

    response = StreamingHttpResponse(
        get_status(user),
        content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["Connection"] = "keep-alive"
    response["X-Accel-Buffering"] = "no"
    return response