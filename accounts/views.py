from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from organizations.views import TenantAPIviews 

from .models import User
from .serializers import UserSignupSerializer , UserLoginSerializer
from rest_framework import status
from .services import Forgot_password_sender , send_verification ,Email_verifier , password_reset_verifier
from django.urls import reverse
from .tasks import send_verification_email , send_Password_Reset_email
from core.auth import authenticate_bearer_by_token
from .selectors import get_status
from django.http import StreamingHttpResponse , HttpResponseForbidden
from organizations.services import Create_Org
from django.contrib.auth import authenticate
from organizations.views import TenantAPIviews
from .services import register_fcm_token
from notification.services import Create_user_Notifications
# Create your views here.

class LoginAPI(TokenObtainPairView):
    authentication_classes = []
    permission_classes = []
    def post(self , request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            response = super().post(request)
            return response
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
            verify_url = ("https://multi-tenant-saas-project-frontend.vercel.app/html/verify.html"f"?uidb64={uid}&token={token}")
            send_verification_email.delay(email = user.email , verify_url=verify_url)
            Create_Org(user = user , name = f"{user.username}'s organization" , type="personal")
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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

class ForgotPasswordSender(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self , request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            uid , token = Forgot_password_sender(user=user)
            reset_url = ("https://multi-tenant-saas-project-frontend.vercel.app/html/reset-password.html"f"?uidb64={uid}&token={token}")
            send_Password_Reset_email.delay(email = user.email , verify_url=reset_url)
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
                         
class Forgot_Password_Reset_API(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self , request):
        if request.user and request.user.is_authenticated:
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password') 

            if authenticate(request , email = request.user.email , password = current_password):
                user = request.user
                user.set_password(new_password)
                user.save(update_fields=['password'])
                return Response({'message':"Password reset successfully"},status=status.HTTP_200_OK)
        else:
            new_password = request.data.get('new_password')
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            user = password_reset_verifier(uidb64=uidb64 , token=token , new_password=new_password)

            if user:
                return Response({'message':"Password reset successfully"},status=status.HTTP_200_OK)
            return Response({"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST)
        
class Password_Reset_API(TenantAPIviews):
    def post(self , request):
        if request.user and request.user.is_authenticated:
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password') 

            if authenticate(request , email = request.user.email , password = current_password):
                user = request.user
                user.set_password(new_password)
                user.save(update_fields=['password'])
                return Response({'message':"Password reset successfully"},status=status.HTTP_200_OK)
            return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterDeviceTokenView(TenantAPIviews):

    def post(self, request):
        token = request.data.get('fcm_token')
        
        if not token:
            return Response({"error": "fcm_token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        register_fcm_token(user=request.user, token=token) 
        
        return Response({"message": "Device token registered successfully"}, status=status.HTTP_200_OK)