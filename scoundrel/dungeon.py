from itertools import product

from .card import ScoundrelCard
from .rank import Rank
from .suit import Suit

def create_dungeon():
    """
    Create a new scoundrel deck.
    """
    return [
        ScoundrelCard(suit, rank)
        for rank, suit in product(Rank, Suit)
        if ScoundrelCard.is_scoundrel(rank, suit)
    ]
