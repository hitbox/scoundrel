from collections import namedtuple

from .rank import Rank
from .suit import Suit

Card = namedtuple('Card', 'suit rank')

class ScoundrelCard(Card):
    """
    A card in a game of scoundrel.
    """

    @staticmethod
    def is_scoundrel(rank, suit):
        """
        Return if rank and suit belongs in scoundrel deck.
        """
        return (
            suit in (Suit.CLUBS, Suit.SPADES)
            or (
                suit in (Suit.HEARTS, Suit.DIAMONDS)
                and rank not in (Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING)
            )
        )

    @property
    def is_weapon(self):
        return self.suit.is_weapon

    @property
    def is_health(self):
        return self.suit.is_health

    @property
    def is_monster(self):
        return self.suit.is_monster

    @property
    def game_string(self):
        """
        Return nice name to display.
        """
        return f'{self.suit.game_name.title()}({self.game_value})'

    @property
    def game_value(self):
        """
        Return value used in the game of scoundrel.
        """
        return self.rank.value
