from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Board
from organizations.views import TenantAPIviews
from workspace.models import Workspace
from .services import Create_Board
from .selectors import get_boards_for_workspace
from core.throttles import OrganizationThrottling
from .serializers import BoardSerializer , BoardCreateSerializer
# Create your views here.

class BoardListCreateAPI(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def get(self , request , workspace_slug):
        workspace = Workspace.objects.get(slug = workspace_slug , organization = request.organization,is_deleted = False)
        boards = get_boards_for_workspace(workspace=workspace)
        serializer = BoardSerializer(boards , many = True)
        return Response(serializer.data)

    def post(self , request , workspace_slug):
        workspace = Workspace.objects.get(slug = workspace_slug , organization = request.organization,is_deleted = False)
        board = Create_Board(workspace=workspace,actor=request.membership,name=request.data.get('name'))
        serializer = BoardCreateSerializer(board)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

