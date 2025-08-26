import os
import random

from configparser import ConfigParser
from configparser import ExtendedInterpolation
from itertools import groupby

from scoundrel import parse
from scoundrel import runner
from scoundrel.align import AlignRelationship
from scoundrel.align import FlexLayout
from scoundrel.card import ScoundrelCard
from scoundrel.choose import ChooseMenu
from scoundrel.constant import CONFIG_KEY
from scoundrel.deck import Deck
from scoundrel.external import pygame
from scoundrel.game import Scoundrel
from scoundrel.message import ScoundrelMessage
from scoundrel.rank import Rank
from scoundrel.suit import Suit
from scoundrel.util import human_split
from scoundrel.util import letter_indexer

from . import layout
from .animation import AnimationManager
from .animation import FrameAnimation
from .animation import get_named_animations
from .assets import Assets
from .relationship import Relationship
from .relationship import RelationshipManager
from .util import create_sprite_from_card
from .util import post_quit

class ScoundrelPygame:

    default_display_size = (600, 600)
    default_framerate = 60
    default_message_generator_class = ScoundrelMessage
    default_menu_class = ChooseMenu
    default_messages_length = 5

    def __init__(
        self,
        assets,
        display_size = None,
        framerate = None,
        message_generator_class = None,
        menu_class = None,
        messages_length = None,
    ):
        self.assets = assets

        if display_size is None:
            display_size = self.default_display_size
        self.display_size = display_size

        if framerate is None:
            framerate = self.default_framerate
        self.framerate = framerate

        if message_generator_class is None:
            message_generator_class = self.default_message_generator_class
        self.message_generator = message_generator_class()

        if menu_class is None:
            menu_class = self.default_menu_class
        self.menu_class = menu_class

        if messages_length is None:
            messages_length = self.default_messages_length
        self.messages_length = messages_length

    @classmethod
    def add_subparser(cls, subparsers):
        """
        Add ScoundrelPygame subparser and arguments.
        """
        subparser = subparsers.add_parser('pygame')
        subparser.add_argument(
            '--display-size',
            type = parse.size,
            default = cls.default_display_size,
            help = 'pygame display size. Default: %(default)s',
        )
        subparser.add_argument(
            '--framerate',
            type = int,
            default = cls.default_framerate,
            help = 'Frames per second. Default: %(default)s',
        )
        subparser.add_argument(
            '--config',
            help = 'Path to config.'
        )
        subparser.set_defaults(
            func = runner.run,
            view_class = cls.from_args,
        )

    @staticmethod
    def validate_args(args):
        if args.framerate < 1:
            raise ValueError('--frame-rate must be positive.')

    @classmethod
    def assets_dict_from_config(cls, cp):
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

    @classmethod
    def from_args(cls, args):
        """
        Scoundrel pygame interface from command line arguments.
        """
        cls.validate_args(args)

        cp = ConfigParser(
            interpolation = ExtendedInterpolation(),
        )
        cp.read(args.config or os.environ.get(CONFIG_KEY))

        assets = cls.assets_dict_from_config(cp)

        instance = cls(
            display_size = args.display_size,
            framerate = args.framerate,
            assets = assets,
        )
        return instance

    def init_pygame(self):
        pygame.font.init()
        self.display_surface = pygame.display.set_mode(self.display_size)
        self.display_rect = self.display_surface.get_rect()
        self.clock = pygame.time.Clock()
        self.ui_font = pygame.font.Font(None, 32)

    def init_listeners(self, game):
        game.on('heal', self.dispatch_flash)
        game.on('player_damage', self.dispatch_flash)

        game.on('init_room', self.on_init_room)
        game.on('move_card', self.on_move_card)
        game.on('game_over', self.hold_last_frame)

    def hold_last_frame(self, event_name, game):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

    def init_game(self, game):
        """
        Initialize interface against game instance.
        """
        self.init_pygame()

        self.animation_manager = AnimationManager()
        self.named_animations = get_named_animations(self.assets)

        self.relationship_manager = RelationshipManager()

        self.message_list = []
        self.sprites = pygame.sprite.Group()

        reference_rect = self.assets['smallcards'][(Suit.DIAMONDS, Rank.ACE)].get_rect()
        self.run_card = create_run_card(reference_rect.size, self.ui_font)

        # Health
        self.health_image = self.assets['suits']['hearts']
        self.health_rect = self.health_image.get_rect()
        self.health_layout = FlexLayout.from_columns(
            tile_width = self.health_rect.width,
            ncols = 10,
            gap = (2,0),
            centerx = self.display_rect.centerx,
            y = 2,
        )

        self.sprite_for_card = {}
        for card in game.decks['dungeon']:
            image = self.assets['smallcards'][(card.suit, card.rank)]
            card_sprite = create_sprite_from_card(card, image)
            card_sprite.animated_sprite = None
            self.sprite_for_card[card] = card_sprite
            if card.is_monster:
                animation = random.choice(list(self.named_animations.values()))
                card_sprite.animated_sprite = create_monster_sprite(animation.frames[0])
                self.animation_manager.add(card_sprite.animated_sprite, animation)
                align_monster_to_card = AlignRelationship(
                    to_index = 0,
                    from_attr = 'midbottom',
                    to_attr = 'midtop',
                )
                relationship = Relationship(
                    card_sprite.rect,
                    card_sprite.animated_sprite.rect,
                    align_monster_to_card,
                )
                self.relationship_manager.append(relationship)

        self.room_layout = FlexLayout.from_columns(
            tile_width = reference_rect.width,
            ncols = 5,
            gap = (2, 0),
            centerx = self.display_rect.centerx,
            y = 150, # TODO
        )

        self.battlefield_layout = FlexLayout.from_columns(
            tile_width = reference_rect.width,
            ncols = 6,
            gap = (-reference_rect.width / 4, -reference_rect.height / 4),
            midtop = self.display_rect.center,
        )

        self.message_layout = FlexLayout(
            origin = self.display_rect.bottomleft,
            axis = 'vertical',
            direction = 'reverse',
            boundary = None,
        )

        self.init_listeners(game)

    def dispatch_flash(self, event_name, game, **kwargs):
        """
        Display whatever message lines
        """
        messagegetter = getattr(self.message_generator, event_name)
        lines = messagegetter(event_name, game, **kwargs)
        for line in lines:
            self.flash(line)

    def on_init_room(self, event_name, game):
        # Initialize the room menu.
        indexed_choices = [
            (index, value, label)
            for index, (value, label)
            in letter_indexer(game.choices_for_turn())
        ]
        self.room_menu = self.menu_class(indexed_choices)

    def on_move_card(self, event_name, game, card, source, dest):
        # Get and update card sprite.
        card_sprite = self.sprite_for_card[card]
        card_sprite.deck = dest

        # Add or remove card sprite for deck. If the room deck, add the
        # associated animated sprite, if one.
        if dest in (Deck.ROOM, Deck.BATTLEFIELD):
            self.sprites.add(card_sprite)
            if card_sprite.animated_sprite:
                if dest == Deck.ROOM:
                    self.sprites.add(card_sprite.animated_sprite)
                else:
                    self.sprites.remove(card_sprite.animated_sprite)
        else:
            self.sprites.remove(card_sprite)
            if card_sprite.animated_sprite:
                self.sprites.remove(card_sprite.animated_sprite)

    def flash(self, message):
        image = self.ui_font.render(message, True, 'white')
        self.message_list.append((image, image.get_rect()))
        if len(self.message_list) > self.messages_length:
            # Keep last three
            self.message_list = self.message_list[-self.messages_length:]

    def _health_rects(self, health_count):
        """
        Instantiate and return rects for health images for a given count.
        """
        health_rects = [self.health_rect.copy() for _ in range(health_count)]
        if health_rects:
            self.health_layout(health_rects)
        return health_rects

    def _max_health_bottom(self):
        health_rects = self._health_rects(Scoundrel.MAX_HEALTH)
        bottom = max(rect.bottom for rect in health_rects)
        return bottom

    def _layout_health(self, game):
        health_rects = self._health_rects(game.health)
        return health_rects

    def sprite_for_choice(self, key):
        if isinstance(key, ScoundrelCard):
            return self.sprite_for_card[key]
        elif key == 'r':
            self.sprites.add(self.run_card)
            return self.run_card

    def layout_room_cards(self, available_choices):
        self.sprites.remove(self.run_card)
        indexed = self.room_menu.menu_lines()
        sprites = [self.sprite_for_choice(option) for _, option, _ in indexed]
        rects = [sprite.rect if sprite else None for sprite in sprites]
        self.room_layout(rects)

    def layout_battlefield(self, game):
        rects = [self.sprite_for_card[card].rect for card in game.decks['battlefield']]
        self.battlefield_layout(rects)

    def render_messages(self):
        """
        Render text messages from bottom-up.
        """
        rects = [rect for image, rect in self.message_list]
        if rects:
            self.message_layout(rects)
            for image, rect in self.message_list:
                self.display_surface.blit(image, rect)

    def _render_frame(self, health_rects):
        # Clear screen
        self.display_surface.fill('black')

        # Draw health
        for rect in health_rects:
            self.display_surface.blit(self.health_image, rect)

        self.render_messages()
        self.sprites.draw(self.display_surface)

        pygame.display.update()

    def get_click_card(self, point):
        for sprite in self.sprites:
            if (
                sprite.card
                and sprite.deck == Deck.ROOM
                and sprite.rect.collidepoint(point)
            ):
                return sprite.card

    def prompt_for_turn(self, game, available_choices):
        """
        Prompt to select card from room.
        """
        self.room_menu.update_for_available(available_choices)

        health_rects = self._layout_health(game)
        self.layout_room_cards(available_choices)
        self.layout_battlefield(game)
        self.relationship_manager.update()

        # Run until card selected for turn and return it.
        elapsed = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Click to return card for single turn in room.
                        card = self.get_click_card(event.pos)
                        if card:
                            #self.message_list.clear()
                            return card

            self.animation_manager.update(elapsed)
            self._render_frame(health_rects)
            elapsed = self.clock.tick(self.framerate)


def create_monster_sprite(image, rect=None):
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = rect or image.get_rect()
    sprite.deck = None
    sprite.card = None
    sprite.room = None
    return sprite

def create_run_card(size, font):
    run_card = pygame.sprite.Sprite()
    run_card.image = pygame.Surface(size)
    run_card.rect = run_card.image.get_rect()
    text_image = font.render('Run', True, 'white')
    text_rect = text_image.get_rect(center=run_card.rect.center)
    run_card.image.blit(text_image, text_rect)
    run_card.card = None
    run_card.deck = None
    return run_card
