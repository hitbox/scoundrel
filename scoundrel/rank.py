from enum import IntEnum

class Rank(IntEnum):
    """
    Enumeration of card ranks.
    """

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def iter_from_ace(cls):
        yield cls.ACE
        yield cls.TWO
        yield cls.THREE
        yield cls.FOUR
        yield cls.FIVE
        yield cls.SIX
        yield cls.SEVEN
        yield cls.EIGHT
        yield cls.NINE
        yield cls.TEN
        yield cls.JACK
        yield cls.QUEEN
        yield cls.KING

    @classmethod
    def list_from_ace(cls):
        return list(cls.iter_from_ace())
