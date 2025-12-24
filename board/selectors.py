from .models import Board

def get_boards_for_workspace(*,workspace):
    boards = Board.objects.filter(
        workspace = workspace,
        organization = workspace.organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')