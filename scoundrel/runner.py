import random

from .card import ScoundrelCard
from .game import Scoundrel

def run(args):
    """
    """
    if args.seed is not None:
        random.seed(args.seed)

    # Build a scoundrel dungeon deck
    dungeon_deck = ScoundrelCard.create_dungeon(half_monsters=args.half_monsters)
    random.shuffle(dungeon_deck)

    # XXX: Messy bit of hard coding.

    interface = args.view_class(args)

    game = Scoundrel.from_args(dungeon_deck, interface, args)
    interface.init_game(game)
    game.play_loop()
