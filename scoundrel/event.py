from enum import Enum

class Event:

    MOVE_CARD = 'move_card'
    INIT_ROOM = 'init_room'
    BEGIN_TURN = 'begin_turn'
    RAN_AWAY = 'ran_away'
    HEAL = 'heal'
    PLAYER_DAMAGE = 'player_damage'
    BATTLE_MONSTER = 'battle_monster'
    GAME_OVER = 'game_over'
