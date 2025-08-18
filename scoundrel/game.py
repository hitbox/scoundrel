from collections import defaultdict

from .card import ScoundrelCard

class Scoundrel:
    """
    State and methods for executing a game of scoundrel.
    """

    MAX_HEALTH = 20

    def __init__(self, dungeon, prompt_for_turn, god_mode=False):
        self.dungeon = dungeon
        self.prompt_for_turn = prompt_for_turn
        self.god_mode = god_mode
        self.room_deck = []
        self.discard_deck = []
        self.battlefield_deck = []
        self.avoided_room = False
        self.health = self.MAX_HEALTH
        self.listeners = defaultdict(list)

    def on(self, event_name, callback):
        """
        Register a listener callback for an event name.
        """
        self.listeners[event_name].append(callback)

    def emit(self, event_name, **event_data):
        """
        Emit event to all listeners.
        """
        for listener in self.listeners[event_name]:
            listener(event_name=event_name, game=self, **event_data)

    def move_card(self, card, source, dest, to_bottom=False):
        """
        Move card from one deck to another.
        """
        source.pop(source.index(card))
        index = 0 if to_bottom else len(dest)
        dest.insert(index, card)
        self.emit('move_card', card=card, source=source, dest=dest)

    def init_room(self):
        """
        Build a room by drawing from the dungeon until the room is filled with
        four cards.
        """
        while self.dungeon and len(self.room_deck) < 4:
            card = self.dungeon[-1]
            self.move_card(card, self.dungeon, self.room_deck)
        self.emit('init_room')

    def begin_turn(self):
        """
        Start of player's turn just after a new room.
        """
        self.emit('begin_turn')

    @property
    def is_new_room(self):
        return len(self.room_deck) == 4

    @property
    def is_avoid_room_available(self):
        """
        True if player did not run last room and this is the start of a new
        room.
        """
        return not self.avoided_room and self.is_new_room

    @property
    def is_dungeon_alive(self):
        return bool(self.dungeon)

    @property
    def is_player_alive(self):
        return self.god_mode or self.health > 0

    @property
    def is_playing(self):
        return self.is_dungeon_alive and self.is_player_alive

    def choices_for_turn(self):
        """
        Create a choices dict for the beginning of a turn.
        """
        choices = []
        for card in self.room_deck:
            choices.append((card, card.game_string))

        # Allow running on first turn and didn't run last room.
        if self.is_avoid_room_available:
            choices.append(('r', 'Run'))

        return choices

    def avoid_room(self):
        """
        Place room cards back in dungeon at the bottom, preserving order.
        """
        self.emit('ran_away')
        self.avoided_room = True
        for card in list(self.room_deck):
            self.move_card(card, self.room_deck, self.dungeon, to_bottom=True)

    def play_card(self, card):
        """
        Take card off room deck and apply card to play deck.
        """
        if card.is_health:
            # Apply health and discard.
            self.apply_health_potion(card)
            self.move_card(card, self.room_deck, self.discard_deck)

        elif card.is_weapon:
            self.equip_weapon(card)

        elif card.is_monster:
            self.battle_monster(card)

    def apply_health_potion(self, health_card):
        """
        Apply health potion card to player.
        """
        heal_value = health_card.game_value
        healed = min(heal_value, self.MAX_HEALTH - self.health)
        self.health += healed
        self.emit('heal', amount=healed, card=health_card)

    def discard_playing_deck(self):
        """
        Move cards from play to discarded.
        """
        while self.battlefield_deck:
            card = self.battlefield_deck[-1]
            self.move_card(card, self.battlefield_deck, self.discard_deck)

    def equip_weapon(self, card):
        """
        Equip weapon card onto playing deck.
        """
        weapon_in_play = self.weapon_in_play()
        if weapon_in_play:
            self.discard_playing_deck()
        self.move_card(card, self.room_deck, self.battlefield_deck)

    def monsters_in_play(self):
        """
        Return all the monster cards in play.
        """
        return [card for card in self.battlefield_deck if card.is_monster]

    def weakest_monster(self):
        """
        Return the lowest value monster card in play.
        """
        return min(self.monsters_in_play(), key=lambda card: card.game_value)

    def weapon_in_play(self):
        """
        Return the equiped weapon card or None.
        """
        for card in self.battlefield_deck:
            if not card.is_weapon:
                # Raise for assumption.
                raise RuntimeError(f'The first card in play must be a weapon.')
            return card

    def get_weapon_for_battle(self, monster_card):
        # If a monster of greater value than the lowest monster already on the
        # weapon is played, the player must fight it barehanded.
        weapon = self.weapon_in_play()
        if self.battlefield_deck:
            monsters_in_play = self.monsters_in_play()
            if not monsters_in_play:
                # Weapon in play, no monsters, player gets to use it.
                return weapon
            else:
                weakest_monster = self.weakest_monster()
                if monster_card.game_value < weakest_monster.game_value:
                    # The played monster has a lesser value than the weakest
                    # already in play. The player uses their weapon to reduce
                    # damage taken.
                    return weapon

    def apply_damage(self, weapon, monster_card):
        """
        Apply damage to player from monster card, reducing it if a weapon is
        used.
        """
        damage = monster_card.game_value
        if weapon:
            # Reduce damage from weapon.
            damage -= weapon.game_value
        if damage > 0:
            self.health -= damage
        self.emit(
            'player_damage',
            damage = damage,
            source = monster_card,
            weapon = weapon,
        )

    def battle_monster(self, monster_card):
        """
        Calculate damage from monster and apply to health.
        """
        weapon = self.get_weapon_for_battle(monster_card)

        # Place monster in play or discard if no equiped weapon card.
        if self.battlefield_deck:
            dest = self.battlefield_deck
        else:
            dest = self.discard_deck
        self.move_card(monster_card, self.room_deck, dest)
        self.apply_damage(weapon, monster_card)

    def loop_step(self):
        """
        A single step in main game loop.
        """
        self.init_room()

        # Play until one card left in the room.
        while self.is_playing and len(self.room_deck) > 1:
            self.begin_turn()
            choices = self.choices_for_turn()
            card_or_run = self.prompt_for_turn(self, choices)
            if isinstance(card_or_run, ScoundrelCard):
                self.play_card(card_or_run)
            else:
                self.avoid_room()

    def play_loop(self):
        """
        Loop until game of scoundrel is done.
        """
        while self.is_playing:
            self.loop_step()
        self.emit('game_over')
