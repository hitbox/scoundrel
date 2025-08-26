from enum import IntEnum

class Suit(IntEnum):
    """
    Enumeration of card suits.
    """

    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def hearts_diamonds_clubs_spades(cls):
        yield cls.HEARTS
        yield cls.DIAMONDS
        yield cls.CLUBS
        yield cls.SPADES

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
