from .models import Card
from board.models import Board
from activities.services import log_Activity

from common.exceptions import PermissionDenied

def Create_Card(*,board,actor,title,description = ''):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("you are not allowed to create cards")

    if board.is_archived:
        raise PermissionDenied("board is archived ")
    
    card =  Card.objects.create(
        organization = board.organization,
        board = board,
        title = title,
        description = description,
    )

    log_Activity(
        organization=board.organization,
        actor=actor,
        action="card_created",
        entity_type='card',
        entity_id=card.id,
        metadata={'title':card.title},
    )

    return card

def Move_Card(*,card,actor,new_status):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    if new_status not in dict(Card.STATUS_CHOICES):
        raise PermissionDenied("This is not a valid status ")
    
    card.status = new_status

    log_Activity(
        organization=card.organization,
        actor=actor,
        action="card_moved",
        entity_type='card',
        entity_id=card.id,
        metadata={'title':card.title},
    )
    card.save(update_fields = ["status"])

    
def Archive_Card(*,card,actor):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    card.is_archived = True
    card.save(update_fields = ["is_archived"])