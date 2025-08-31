import os

from configparser import ConfigParser
from configparser import ExtendedInterpolation
from itertools import chain
from itertools import product

from scoundrel.constant import CONFIG_KEY
from scoundrel.external import pygame
from scoundrel.rank import Rank
from scoundrel.suit import Suit
from scoundrel.util import human_split
from scoundrel.view.pygame.rect_grid import RectGrid

from .util import strip_alpha

class Assets:

    default_prefix = 'spritesheet.'

    def __init__(self, source, images, scale, rect_grid):
        self.source = source
        self.images = images
        self.scale = scale
        self.rect_grid = rect_grid

    @classmethod
    def from_args(cls, args):
        """
        Assets from command line arguments.
        """
        # confif path from arguments or environment.
        config = args.config or os.environ.get(CONFIG_KEY)
        cp = ConfigParser(
            interpolation = ExtendedInterpolation(),
        )
        cp.read(config)
        section = cp[args.section]
        return cls.from_config(section)

    @classmethod
    def from_config(cls, section):
        path = section['path']
        sheet_image = pygame.image.load(path)
        rect_grid = RectGrid.from_config(section)
        scale = int(section.get('scale', '1'))
        grid = eval(section['types'])
        strip = section.getboolean('strip')
        container = section.get('container', None)
        if isinstance(container, str):
            container = pygame.Rect(eval(container))
        elif container is None:
            container = sheet_image.get_rect()

        if rect_grid.columnwise:
            subrects = rect_grid.iter_rects_columnwise(container)
        else:
            subrects = rect_grid.iter_rects(container)

        assets = {}
        for key, subrect in zip(grid, subrects):
            tile_image = sheet_image.subsurface(subrect).copy()

            if strip:
                tile_image = strip_alpha(tile_image)

            if scale > 1:
                subrect = pygame.Rect(subrect)
                size = tuple(map(lambda d: d * scale, subrect.size))
                tile_image = pygame.transform.scale(tile_image, size)
            assets[key] = tile_image

        # Instantiate and return class.
        instance = cls(sheet_image, assets, scale, rect_grid)
        return instance

    @classmethod
    def from_config_many(cls, cp, suffixes, prefix=None):
        """
        Many Assets instances from names and a prefix from config.
        """
        if prefix is None:
            prefix = cls.default_prefix

        for suffix in suffixes:
            section_name = f'{prefix}{suffix}'
            section = cp[section_name]
            instance = cls.from_config(section)
            yield (suffix, instance)


def scoundrel_assets_from_config(cp):
    # Strictly build a dictionary from the suffixes referencing other sections
    # in the config. Raise for existing keys.
    assets = {}
    suffixes = human_split(cp['pygame_user_interface']['spritesheets'])
    for suffix, assets_instance in Assets.from_config_many(cp, suffixes):
        if suffix not in assets:
            assets[suffix] = {}
        # Strictly update dict.
        for key, image in assets_instance.images.items():
            if key in assets[suffix]:
                raise KeyError
            assets[suffix][key] = image
    return assets
