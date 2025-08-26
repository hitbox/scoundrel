class ScoundrelMessage:
    """
    """

    def __init__(self, indent=None):
        if indent is None:
            indent = ' ' * 2
        self.indent = indent

    def ran_away(self, event_name, game):
        return [f'You run from the room.']

    def heal(self, event_name, game, amount, card):
        return [f'You healed for {amount}.']

    def init_room(self, event_name, game):
        return [f'You step into a new room.']

    def player_damage(self, event_name, game, damage, source, weapon):
        if damage <= 0:
            message = (
                f'Your weapon avoids all damage from {source.game_string}!')
        else:
            if source.game_value == damage:
                message = (
                    f'{source.game_string} does full damage!')
            else:
                message = (
                    f'{damage} damage from {source.game_string}.')
        return [message]

    def generic_alert(self, **kwargs):
        return [f'{kwargs}']

    def alert_begin_turn(self, event_name, game):
        """
        Cards in play on the battlefield.
        """
        if not game.decks.cards('battlefield'):
            return ['The battlefield awaits you']
        else:
            lines = ['Battlefield']
            for card in game.decks.cards('battlefield'):
                lines.append(f'{self.indent}{card.game_string}')
            return lines

    def game_over_alert(self, event_name, game):
        if game.is_player_alive:
            return ['You win!']
        else:
            return ['You died']
