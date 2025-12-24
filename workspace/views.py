from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import Create_Workspace , Archive_Workspace
from .selectors import get_workspace_for_org
from .serializers import WorkspaceSerializer
# Create your views here.
class WorkspaceListCreateAPI(APIView):
    def get(self , request):
        if not request.organization:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        qs = get_workspace_for_org(organization=request.organization)
        serializer = WorkspaceSerializer(qs , many = True)
        return Response(serializer.data)

    def post(self , request):
        workspace = Create_Workspace(
            organization=request.organization,
            actor=request.membership,
            name=request.data.get('name'),
        )
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer,status=status.HTTP_201_CREATED)

