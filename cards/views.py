from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.exceptions import ValidationError

from .models import Card
from board.models import Board
from .selectors import get_card_for_board , get_Cards , get_Cards_for_workspace
from .services import Create_Card , Update_Card , Delete_card
from .serializers import CardSerializer , CardCreateSerializer
from organizations.views import TenantAPIviews
# Create your views here.

class CardListCreateAPI(TenantAPIviews):
    def get(self,request,board_slug):
        board = Board.objects.get(
            slug = board_slug,
            organization = request.organization,
            is_deleted = False,
        )
        cards = get_card_for_board(board=board)
        serializer = CardSerializer(cards , many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
    
    def post (self , request , board_slug):
        board = Board.objects.get(
            slug = board_slug,
            organization = request.organization,
            is_deleted = False,
        )

        serializer = CardCreateSerializer(data = request.data)
        if serializer.is_valid():
            card = Create_Card(
                board=board,
                actor=request.membership,
                assignee = request.user,
                serializer=serializer.validated_data
            )
            serializer = CardSerializer(card)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        raise ValidationError("invalid data ")
    
class CardListForOrg(TenantAPIviews):
    def get(self , request):
        cards = get_Cards(actor = request.membership , organization = request.organization)
        serializer = CardSerializer(cards , many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)

class CardUpdateAPI(TenantAPIviews):
    def put(self , request , card_slug):
        
        title = request.data.get('title',None)
        description = request.data.get('description',None)
        status_ = request.data.get('status',None)
        try:
            print(title,description,status_)
            card = Update_Card(slug = card_slug , actor = request.membership , title = title , description = description , status = status_)
            return Response({"message": "Card updated successfully"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"error":"invalid request"} , status=status.HTTP_400_BAD_REQUEST)
        
class CardListForWorkspace(TenantAPIviews):
    def get(self , request , workspace_slug):
        cards = get_Cards_for_workspace(actor = request.membership , organization = request.organization , workspace_slug = workspace_slug)
        serializer = CardSerializer(cards , many = True)
        return Response(serializer.data , status=status.HTTP_202_ACCEPTED)

class CardDeleteAPI(TenantAPIviews):
    def delete(self , request , card_id):

        Delete_card(id = card_id , actor = request.membership)

        return Response({"message": "Card deleted successfully"}, status=status.HTTP_204_NO_CONTENT)