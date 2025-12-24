from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Card
from board.models import Board
from .selectors import get_card_for_board
from .services import Create_Card
from .serializers import CardSerializer
# Create your views here.

class CardListCreateAPI(APIView):
    def get(self,request,board_id):
        board = Board.objects.get(
            id = board_id,
            organization = request.organization,
            is_deleted = False,
        )
        cards = get_card_for_board(board=board)
        serializer = CardSerializer(cards , many = True)
        return Response(serializer)
    
    def post (self , request , board_id):
        board = Board.objects.get(
            id = board_id,
            organization = request.organization,
            is_deleted = False,
        )
        card = Create_Card(
            board=board,
            actor=request.membership,
            title = request.data.get('title'),
            description=request.data.get('description',""),
        )
        serializer = CardSerializer(card)
        return Response(serializer , status=status.HTTP_201_CREATED)