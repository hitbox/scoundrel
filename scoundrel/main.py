import random

from .argument_parser import argument_parser
from .dungeon import create_dungeon
from .game import Scoundrel
from .view import ScoundrelTUI

def main(argv=None):
    """
    Command line interface.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    # Build a scoundrel dungeon deck
    dungeon_deck = create_dungeon()
    random.shuffle(dungeon_deck)

    # Run a scoundrel game with a text interface.
    interface = ScoundrelTUI()
    game = Scoundrel(
        dungeon_deck,
        interface.prompt_for_turn,
        god_mode = args.god,
    )
    interface.init_game(game)
    game.play_loop()
