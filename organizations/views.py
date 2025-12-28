from rest_framework.views import APIView
from common.exceptions import PermissionDenied
from .selectors import get_org_for_user
from .services import Create_Org
from .serializers import Organization_Serializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here

class TenantAPIviews(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
    
        if not request.membership:
            return PermissionDenied("you cannot access this organization")
        
class Organization_List_API(APIView):
    def get(self , request):
        qs = get_org_for_user(user=request.user)
        serializer = Organization_Serializer(qs ,  many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    
class Organization_Create_API(APIView):
    def post(self , request):
        serializer = Organization_Serializer(data = request.data)
        if serializer.is_valid():
            organization = Create_Org(user=request.user , name=serializer.validated_data['name'] , type=serializer.validated_data['type'])
            serializer = Organization_Serializer(organization)
            return Response(serializer.data , status=status.HTTP_201_CREATED)