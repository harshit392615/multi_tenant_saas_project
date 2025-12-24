from .models import Card

def get_card_for_board(*,board):
    return Card.objects.filter(
        board = board,
        organization = board.organization,
        is_archived = False,
        is_deleted = False,
    ).order_by('created_at')