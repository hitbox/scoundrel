import os

from configparser import ConfigParser
from configparser import ExtendedInterpolation
from itertools import chain
from itertools import product

from scoundrel.external import pygame
from scoundrel.rank import Rank
from scoundrel.suit import Suit
from scoundrel.view.pygame import layout
from scoundrel.view.pygame.assets import Assets
from scoundrel.view.pygame.rect_grid import RectGrid
from scoundrel.util import human_split

class AssetBrowser:
    """
    Interactive pygame asset browser.
    """

    def __init__(self, assets):
        self.assets = assets

    @classmethod
    def add_subparser(cls, subparsers):
        parser = subparsers.add_parser('assets')
        parser.add_argument(
            'section',
        )
        parser.add_argument(
            '--config',
        )
        parser.set_defaults(func=cls.from_args)

    @classmethod
    def from_args(cls, args):
        assets = Assets.from_args(args)
        return cls(assets)

    def make_group(self, window, with_font=None):
        text_images = {}
        widest_text = 0

        if with_font:
            for key, image in self.assets.images.items():
                text_images[key] = with_font.render(f'{key}', True, 'purple')
            text_rects = {
                key: text_image.get_rect()
                for key, text_image in zip(self.assets.images.keys(), text_images.values())
            }
            widest_text = max(rect.width for rect in text_rects.values())

        rects = [image.get_rect() for image in self.assets.images.values()]
        widest_rect = max(rect.width for rect in rects)

        gap = (max(widest_text, widest_rect), 24)
        layout.horizontal(rects, gap_x=gap[0])

        # Align sprites
        # Need config here:
        ncols = 3
        nrows = 4
        container = pygame.Rect(
            0, 0,
            gap[0] * ncols + self.assets.rect_grid.tile_size[0] * self.assets.scale * ncols,
            gap[1] * nrows * self.assets.rect_grid.tile_size[1] * self.assets.scale * nrows,
        )
        layout.horizontal_wrap(rects, container, gap=gap)
        layout.move_as_group(rects, center=window.center)

        group = pygame.sprite.Group()
        for (key, image), rect in zip(self.assets.images.items(), rects):
            tile_sprite = pygame.sprite.Sprite(group)
            tile_sprite.image = image
            tile_sprite.rect = rect

            if with_font:
                text_sprite = pygame.sprite.Sprite(group)
                text_sprite.image = with_font.render(f'{key}', True, 'purple')
                text_sprite.rect = text_sprite.image.get_rect(midtop=tile_sprite.rect.midbottom)

        return group

    def run(self):
        """
        Display images from sprite sheet on grid. Drag to move.
        """
        pygame.font.init()
        display = pygame.display.set_mode((1900, 900))
        window = display.get_rect()
        clock = pygame.time.Clock()

        ui_font = pygame.font.Font(None, 24)
        group = self.make_group(window, ui_font)

        offset = pygame.Vector2(0, 0)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        offset += event.rel

            display.fill('black')
            for sprite in group:
                display.blit(sprite.image, sprite.rect.move(offset))

            pygame.display.update()

            clock.tick(60)
