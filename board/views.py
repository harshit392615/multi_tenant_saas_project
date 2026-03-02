from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Board
from organizations.views import TenantAPIviews
from workspace.models import Workspace
from .services import Create_Board , Delete_Board
from .selectors import get_boards_for_workspace , get_Boards , get_board_for_slug
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

class Board_List_For_Org(TenantAPIviews):
   throttle_classes = [OrganizationThrottling]
   def get(self , request):
      notes = get_Boards(actor = request.membership , organization = request.organization)
      serializer = BoardSerializer(notes , many = True)
      return Response(serializer.data , status = status.HTTP_202_ACCEPTED)
   
class BoardDetailsAPI(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def get(self , request , board_slug):
        board = get_board_for_slug(board_slug = board_slug , organization = request.organization)
        serializer = BoardSerializer(board)
        return Response(serializer.data , status=status.HTTP_200_OK)
   
class Board_Delete_API(TenantAPIviews):
    throttle_classes = [OrganizationThrottling]
    def delete(self , request , board_id):
        try:
            Delete_Board(id=board_id , actor=request.membership)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : str(e)},status=status.HTTP_400_BAD_REQUEST)