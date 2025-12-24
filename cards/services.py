from .models import Card
from board.models import Board

from common.exceptions import PermissionDenied

def Create_Card(*,board,actor,title,description = ''):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("you are not allowed to create cards")

    if board.is_archived:
        raise PermissionDenied("board is archived ")
    
    return Card.objects.create(
        board = board,
        title = title,
        description = description,
    )
def Move_Card(*,card,actor,new_status):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    if new_status not in dict(Card.STATUS_CHOICES):
        raise PermissionDenied("This is not a valid status ")
    
    card.status = new_status
    card.save(update_fields = ["status"])

    
def Archive_Card(*,card,actor):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    card.is_archived = True
    card.save(update_fields = ["is_archived"])