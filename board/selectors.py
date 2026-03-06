from .models import Board
from enum import Enum
from common.exceptions import PermissionDenied

class UserRole(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"

def get_boards_for_workspace(*,workspace):
    boards = Board.objects.filter(
        workspace = workspace,
        organization = workspace.organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')

    return boards

def get_Boards(actor , organization):
    if actor.role not in [UserRole.OWNER , UserRole.ADMIN , UserRole.MEMBER , UserRole.VIEWER]:
        raise PermissionDenied("you are not allowed to perform this action")
    boards = Board.objects.filter(
        organization = organization
    )
    
    return boards
def get_board_for_slug(*,actor,board_slug , organization):
    if actor.role not in [UserRole.OWNER , UserRole.ADMIN , UserRole.MEMBER , UserRole.VIEWER]:
        raise PermissionDenied("you are not allowed to perform this action")
    board = Board.objects.get(
            slug = board_slug,
            organization = organization,
            is_deleted = False,
            is_archived = False,
        )
    return board