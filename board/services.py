from .models import Board
from common.exceptions import PermissionDenied ,ValidationError 

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

def Delete_Board(*,id,actor):
    if actor.role not in ['owner','admin']:
        raise PermissionDenied("you are not allowed to perform this action")
    
    try:
        board = Board.objects.get(
            id = id 
        )
    except Board.DoesNotExist: 
        raise ValidationError("invalid organization id")
    
    board.is_deleted =  True

    board.save(update_fields=['is_deleted'])
    return 1