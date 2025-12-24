from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Board
from workspace.models import Workspace
from .services import Create_Board
from .selectors import get_boards_for_workspace
from .serializers import BoardSerializer
# Create your views here.

class BoardListCreateAPI(APIView):
    def get(self , request , workspace_id):
        workspace = Workspace.objects.get(id = workspace_id , organization = request.organization,is_deleted = False)
        boards = get_boards_for_workspace(workspace=workspace)
        serializer = BoardSerializer(boards , many = True)
        return Response(serializer)

    def post(self , request ):
        workspace = Workspace.objects.get(id = workspace_id , organization = request.organization,is_deleted = False)
        board = Create_Board(workspace=workspace,actor=request.membership,name=request.data.get('name'))
        serializer = BoardSerializer(board)
        return Response(serializer , status=status.HTTP_201_CREATED)

