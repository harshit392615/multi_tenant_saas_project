from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.exceptions import ValidationError

from .models import Card
from board.models import Board
from .selectors import get_card_for_board
from .services import Create_Card , Update_Card
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

class CardUpdateAPI(TenantAPIviews):
    def put(self , request , card_slug):

        serializer = CardCreateSerializer(data = request.data)
        if serializer.is_valid():
            card = Update_Card(slug = card_slug , actor = request.membership , serializer=serializer.validated_data)

            serializer = CardSerializer(card)

            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)