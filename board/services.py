from .models import Board
from common.exceptions import PermissionDenied

def Create_Board(*,workspace,actor,name):
    if actor.role not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to make a Board")
    
    if workspace.is_archived:
        raise PermissionDenied("Workspace is archived")
    
    return Board.objects.create(
        name = name,
        workspace = workspace,
    )

def Archive_Board(*,board,actor):
    if actor not in ['owner','admin','member']:
        raise PermissionDenied("You are not allowed to archive this board")
    
    board.is_archived = True
    board.save(update_fields = ['is_archived'])