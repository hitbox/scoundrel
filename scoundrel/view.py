import sys

from .util import letter_indexer

INDENT = '  '

class ScoundrelTUI:
    """
    Scoundrel text user interface.
    """

    def __init__(self, stream=None):
        self._stream = stream

    @property
    def stream(self):
        stream = self._stream
        if stream is None:
            stream = sys.stdout
        return stream

    def init_game(self, game):
        game.on('player_damage', self.alert_damage_taken)
        game.on('begin_turn', self.alert_battlefield_deck)
        game.on('play_card', self.generic_alert)
        game.on('ran_away', self.generic_alert)
        game.on('game_over', self.game_over_alert)

    def alert_damage_taken(self, event_name, game, damage, source, weapon):
        if source.game_value == damage:
            self.stream.write(f'{source.game_string} does full damage!\n')
        else:
            self.stream.write(f'{damage} damage from {source.game_string}.\n')

    def generic_alert(self, **kwargs):
        self.stream.write(f'{kwargs}\n')

    def alert_battlefield_deck(self, event_name, game):
        # Print playing
        if game.battlefield_deck:
            self.stream.write('Playing\n')
            for card in game.battlefield_deck:
                self.stream.write(f'{INDENT}{card.game_string}\n')

    def game_over_alert(self, event_name, game):
        if game.is_player_alive:
            self.stream.write('You win!\n')
        else:
            self.stream.write('You died\n')

    def prompt_for_turn(self, game, choices):
        """
        Build choices for a turn of scoundrel and prompt until valid response.
        """
        prompt = f'Health x {game.health}> '

        indexed = letter_indexer(choices)
        indexed = [(index, value, label) for index, (value, label) in indexed]

        while True:
            self.stream.write('Choose card from room\n')
            for index, _, label in indexed:
                self.stream.write(f'({index}) {label}\n')

            response = input(prompt)
            for index, value, _ in indexed:
                if response == index:
                    return value
            else:
                self.stream.write(f'Invalid input: {response}\n')
