from http import request
from rest_framework.views import APIView
from common.exceptions import PermissionDenied
from .selectors import get_org_for_user , get_memebrship_for_org , get_org_subscription
from .services import Create_Org , Update_Org , Delete_Org , Archive_Org , Add_Membership , Update_Membership , Add_Subscription , Verify_Subscription, delete_Membership
from .serializers import Organization_Create_Serializer , Organization_Update_Serializer , Organization_Archive_Serializer , Organization_Serializer , Membership_add_update , Membership_Get  , Subscription_Serializer
from rest_framework import status
from rest_framework.response import Response
from .models import Membership
from django.http import HttpResponseForbidden
from core.throttles import OrganizationThrottling
from notification.tasks import send_user_notification
from core.redis_sync import redis_client
import json
from django.shortcuts import render
from django.shortcuts import redirect
from core.auth import authenticate_bearer_by_token
from django.http import StreamingHttpResponse , HttpResponseForbidden
\
# Create your views here

class TenantAPIviews(APIView):
    def initial(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.membership = Membership.objects.get(user = request.user , organization = request.organization)
            except Membership.DoesNotExist:
                return HttpResponseForbidden('No access to this organization')
        else:
            request.membership = None 
        super().initial(request, *args, **kwargs)

        if not request.membership:
            return PermissionDenied("you cannot access this organization")
        
class Organization_List_API(APIView):
    def get(self , request):
        qs = get_org_for_user(user=request.user)
        serializer = Organization_Serializer(qs ,  many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    
class Organization_Create_API(APIView):
    throttle_classes = [OrganizationThrottling]
    def post(self , request):
        serializer = Organization_Create_Serializer(data = request.data)
        if serializer.is_valid():
            organization = Create_Org(user=request.user , name=serializer.validated_data['name'] , type=serializer.validated_data['type'])
            serializer = Organization_Serializer(organization)
            send_user_notification.delay("title" , "deiption" , request.user.id)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
class Organization_Update_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def put(self , request):
        serializer = Organization_Update_Serializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
            organization = Update_Org(slug = serializer.validated_data['slug'],actor=request.membership , name=serializer.validated_data['name'])
            serializer = Organization_Update_Serializer(organization)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class Organization_Delete_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def delete(self , request , org_id):
        try:
            Delete_Org(id=org_id , actor=request.membership)
            return Response({"message": "Organization deleted successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class Organization_Archive_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def put(self , request):
        serializer = Organization_Archive_Serializer(data = request.data)
        if serializer.is_valid():
            Archive_Org(slug=serializer.validated_data['slug'] , actor=request.membership)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class Organization_Membership_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def get(self , request):
        memberships = get_memebrship_for_org(request.membership , request.organization)
        data = []
        for membership in memberships:
            mem = {   # NEW dict every loop
                "username": membership.user.username,
                "role": membership.role,
                "email": membership.user.email,
                "status": redis_client.exists(f"user:online:{membership.user.id}")
            }
            data.append(mem)

        serializer = Membership_Get(data , many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        serializer = Membership_add_update(data = request.data)
        if serializer.is_valid():
            membership = Add_Membership(request.membership , request.organization , serializer.validated_data)
            return Response({"message": "Member added successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        email = request.data.get('email')
        if email:
            membership = delete_Membership(request.membership , request.organization , email)
            return Response({"message": "Member removed successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class Organization_Membership_Update_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def put(self,request):
        body = request.data
        print(body)
        serializer = Membership_add_update(data = request.data)
        if serializer.is_valid():
            membership = Update_Membership(request.membership , request.organization , serializer.validated_data)
            return Response({"message": "Member updated successfully"},status=status.HTTP_202_ACCEPTED)
        return Response({"error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Organization_Subscription(TenantAPIviews):
    def get(self , request):
        subscription = get_org_subscription(request.membership , request.organization)
        serializer = Subscription_Serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self , request):
        data = json.loads(request.body)
        print(data)
        context = Add_Subscription(request.user,request.membership , request.organization , data)

        return Response(context , status=status.HTTP_201_CREATED)
    

class Organization_Verify_Subscription(TenantAPIviews):
    permission_classes = []
    def post(self , request):
        data = request.POST

        url = Verify_Subscription(data)

        return redirect(url)
    
# def Get_Active_user(request):
#     token = request.GET.get('token')
#     print(token)
#     try:
#         user = authenticate_bearer_by_token(token)
#     except Exception:
#         return HttpResponseForbidden("Unauthorized")

#     response = StreamingHttpResponse(
#         get_active_users(user),
#         content_type="text/event-stream"
#     )
#     response["Cache-Control"] = "no-cache"
#     response["Connection"] = "keep-alive"
#     response["X-Accel-Buffering"] = "no"
#     return response

### make a json object in redis cache in which active user of a organization will be store and using sse that json will be sended to frontend where all status of user in that jsonn will se setted active else inactive  