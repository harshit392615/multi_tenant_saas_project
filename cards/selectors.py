from .models import Card
from common.exceptions import PermissionDenied
from workspace.models import Workspace

def get_card_for_board(*,board):
    return Card.objects.filter(
        board = board,
        organization = board.organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')

def get_Cards(actor , organization):
    if actor.role not in ['owner','admin','member','viewer']:
        raise PermissionDenied("you are not allowed to perform this action")
    cards = Card.objects.filter(
        organization = organization
    )
    return cards

def get_Cards_for_workspace(actor , organization , workspace_slug):
    if actor.role not in ['owner','admin','member','viewer']:
        raise PermissionDenied("you are not allowed to perform this action")
    
    workspace = Workspace.objects.get(
        slug = workspace_slug,
    )
    cards = Card.objects.filter(
        organization = organization,
        workspace = workspace
    )
    return cards