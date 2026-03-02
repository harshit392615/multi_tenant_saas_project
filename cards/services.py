from .models import Card
from board.models import Board
from activities.services import log_Activity

from common.exceptions import PermissionDenied

def Create_Card(*,board,actor,assignee,serializer):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("you are not allowed to create cards")

    if board.is_archived:
        raise PermissionDenied("board is archived ")
    
    card =  Card.objects.create(
        organization = board.organization,
        board = board,
        workspace = board.workspace,
        assignee = assignee,
        **serializer
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

def Update_Card(* ,slug,actor,title = None , description = None , status = None):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    card = Card.objects.get(
        slug = slug
    )
    
    if title:
        card.title = title
    if description:
        card.description = description
    if status:
        if status not in dict(Card.STATUS_CHOICES):
            raise PermissionDenied("This is not a valid status ")
        card.status = status
        
    card.save() 
    
    log_Activity(
        organization=card.organization,
        actor=actor,
        action="card_moved",
        entity_type='card',
        entity_id=card.id,
        metadata={'title':card.title},
    )

    return card

def Delete_card(*,id,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("You are not allowed to delete cards")
    
    card = Card.objects.get(
        id = id
    )

    card.is_deleted = True

    card.save() 
    
    log_Activity(
        organization=card.organization,
        actor=actor,
        action="card_Deleted",
        entity_type='card',
        entity_id=card.id,
        metadata={'title':card.title},
    )

    return 1
    
def Archive_Card(*,card,actor):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to change status")
    
    card.is_archived = True
    card.save(update_fields = ["is_archived"])