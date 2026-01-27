from rest_framework.views import APIView
from common.exceptions import PermissionDenied
from .selectors import get_org_for_user , get_memebrship_for_org
from .services import Create_Org , Update_Org , Delete_Org , Archive_Org , Add_Update_Membership
from .serializers import Organization_Create_Serializer , Organization_Update_Serializer , Organization_Archive_Serializer , Organization_Serializer , Membership_add_update , Membership_Get
from rest_framework import status
from rest_framework.response import Response
from .models import Membership
from django.http import HttpResponseForbidden
from core.throttles import OrganizationThrottling
from notification.tasks import send_user_notification

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
    throttle_classes = [OrganizationThrottling]
    def get(self , request):
        qs = get_org_for_user(user=request.user)
        serializer = Organization_Serializer(qs ,  many = True)
        # send_user_notification.delay("title" , "description" , request.user.id)
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
            return Response(status=status.HTTP_202_ACCEPTED)
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
            }
            data.append(mem)

        serializer = Membership_Get(data , many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        serializer = Membership_add_update(data = request.data)
        if serializer.is_valid():
            membership = Add_Update_Membership(request.membership , request.organization , serializer.validated_data)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# add membership update api