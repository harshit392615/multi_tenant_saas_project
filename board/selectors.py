from .models import Board
from common.exceptions import PermissionDenied

def get_boards_for_workspace(*,workspace):
    boards = Board.objects.filter(
        workspace = workspace,
        organization = workspace.organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')

    return boards

def get_Boards(actor , organization):
    if actor.role not in ['owner','admin','member','viewer']:
        raise PermissionDenied("you are not allowed to perform this action")
    boards = Board.objects.filter(
        organization = organization
    )
    
    return boards
def get_board_for_slug(*,board_slug , organization):
    board = Board.objects.get(
            slug = board_slug,
            organization = organization,
            is_deleted = False,
            is_archived = False,
        )
    return board