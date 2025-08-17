from enum import Enum

class Suit(Enum):
    """
    Enumeration of card suits.
    """

    CLUBS = 'clubs'
    DIAMONDS = 'diamonds'
    HEARTS = 'hearts'
    SPADES = 'spades'

    @property
    def is_weapon(self):
        return self == Suit.DIAMONDS

    @property
    def is_health(self):
        return self == Suit.HEARTS

    @property
    def is_monster(self):
        return self in (Suit.CLUBS, Suit.SPADES)

    @property
    def game_name(self):
        if self.is_weapon:
            return 'weapon'
        elif self.is_health:
            return 'health'
        elif self.is_monster:
            return 'monster'
