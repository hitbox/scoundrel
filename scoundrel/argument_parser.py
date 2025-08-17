import argparse
import os

def argument_parser():
    """
    Create argument parser.
    """
    prog = os.path.basename(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(
        description = 'Play a game of scoundrel.',
        prog = prog,
    )

    parser.add_argument(
        '--seed',
        type = int,
        help = 'Set random seed value.',
    )

    parser.add_argument(
        '--god',
        action = 'store_true',
        help = 'Invincible player mode.',
    )

    return parser
