import sys

from .choose import ChooseMenu
from .util import letter_indexer

INDENT = '  '

class ScoundrelTUI:
    """
    Scoundrel text user interface.
    """

    def __init__(self, stream=None, menu_class=None):
        self._stream = stream

        if menu_class is None:
            menu_class = ChooseMenu
        self.menu_class = menu_class

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
        game.on('init_room', self.init_room)
        game.on('heal', self.alert_heal)
        game.on('ran_away', self.alert_ran_away)

    def alert_ran_away(self, event_name, game):
        self.stream.write(f'\nYou run from the room.\n')

    def alert_heal(self, event_name, game, amount, card):
        self.stream.write(f'\nYou healed for {amount}.\n')

    def init_room(self, event_name, game):
        """
        Alert for new room and build menu.
        """
        self.stream.write(f'\nYou step into a new room.\n')
        indexed_choices = [
            (index, value, label)
            for index, (value, label)
            in letter_indexer(game.choices_for_turn())
        ]
        self.room_menu = self.menu_class(indexed_choices)

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
        if not game.decks.cards('battlefield'):
            self.stream.write('\nThe battlefield awaits you\n')
        else:
            self.stream.write('\nBattlefield\n')
            for card in game.decks.cards('battlefield'):
                self.stream.write(f'{INDENT}{card.game_string}\n')

    def prompt_for_turn(self, game, available_choices):
        """
        Build choices for a turn of scoundrel and prompt until valid response.
        """
        # Update menu for available choices.
        self.room_menu.update_for_available(available_choices)

        # Loop until valid choice.
        while True:
            self.stream.write('\nChoose card from room\n')
            indexed = self.room_menu.menu_lines()
            for index, value, label in indexed:
                if index is None:
                    index = ' '
                self.stream.write(f'({index}) {label}\n')

            response = input(f'Health x {game.health}> ')

            if response in self.room_menu.chosen_indexes:
                self.stream.write(f'Already played\n')
            elif response in self.room_menu.unavailable:
                self.stream.write(f'Unavailable\n')
            else:
                value = self.room_menu.value_for_index(response)
                if value:
                    self.room_menu.pick(index)
                    return value

                self.stream.write(f'Invalid input: {response}\n')

    def game_over_alert(self, event_name, game):
        if game.is_player_alive:
            self.stream.write('You win!\n')
        else:
            self.stream.write('You died\n')
