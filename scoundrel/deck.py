class DeckManager:

    def __init__(self, *deck_names):
        self._decks = {key: [] for key in deck_names}

    def set_deck(self, name, deck):
        self._decks[name] = deck

    def length(self, deck_name):
        return len(self._decks[deck_name])

    def top_card(self, deck_name):
        return self._decks[deck_name][-1]

    def move_card(self, card, srcname, dstname, to_bottom=False):
        """
        Move card from one deck to another.
        """
        src = self._decks[srcname]
        dst = self._decks[dstname]

        src.pop(src.index(card))
        index = 0 if to_bottom else len(dst)
        dst.insert(index, card)

    def cards(self, deck_name):
        return self._decks[deck_name]
