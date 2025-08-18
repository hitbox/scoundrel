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
        game.on('begin_turn', self.alert_begin_turn)
        game.on('play_card', self.generic_alert)
        game.on('ran_away', self.generic_alert)
        game.on('game_over', self.game_over_alert)
        game.on('init_room', self.alert_init_room)
        game.on('heal', self.alert_heal)
        game.on('ran_away', self.alert_ran_away)

    def alert_ran_away(self, event_name, game):
        self.stream.write(f'\nYou run from the room.\n')

    def alert_heal(self, event_name, game, amount, card):
        self.stream.write(f'\nYou healed for {amount}.\n')

    def alert_init_room(self, event_name, game):
        self.stream.write(f'\nYou step into a new room.\n')

    def alert_damage_taken(self, event_name, game, damage, source, weapon):
        if damage <= 0:
            self.stream.write(
                f'\nYour weapon avoids all damage from {source.game_string}!\n')
        else:
            if source.game_value == damage:
                self.stream.write(
                    f'\n{source.game_string} does full damage!\n')
            else:
                self.stream.write(
                    f'\n{damage} damage from {source.game_string}.\n')

    def generic_alert(self, **kwargs):
        self.stream.write(f'{kwargs}\n')

    def alert_begin_turn(self, event_name, game):
        """
        Cards in play on the battlefield.
        """
        if not game.battlefield_deck:
            self.stream.write('\nThe battlefield awaits you\n')
        else:
            self.stream.write('\nBattlefield\n')
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
            self.stream.write('\nChoose card from room\n')
            for index, _, label in indexed:
                self.stream.write(f'({index}) {label}\n')

            response = input(prompt)
            for index, value, _ in indexed:
                if response == index:
                    return value
            else:
                self.stream.write(f'Invalid input: {response}\n')
