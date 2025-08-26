import argparse
import os

from .game import Scoundrel
from .view import AssetBrowser
from .view import ScoundrelPygame
from .view import ScoundrelTUI

def argument_parser():
    """
    Create argument parser.
    """
    prog = os.path.basename(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(
        description = 'Play a game of scoundrel.',
        prog = prog,
    )
    Scoundrel.add_arguments(parser)

    subparsers = parser.add_subparsers(title='interface', required=True)
    ScoundrelTUI.add_subparser(subparsers)
    ScoundrelPygame.add_subparser(subparsers)
    AssetBrowser.add_subparser(subparsers)

    return parser
