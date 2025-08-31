from scoundrel.external import pygame

class MonsterSprite(pygame.sprite.Sprite):

    def __init__(
        self,
        image,
        *groups,
        rect = None,
        deck = None,
        card = None,
        room = None,
    ):
        super().__init__(*groups)
        self.image = image
        self.rect = rect or self.image.get_rect()
        self.deck = deck
        self.card = card
        self.room = room


def create_run_card(size, font, *groups):
    image = pygame.Surface(size)
    run_card = MonsterSprite(image, *groups)
    text_image = font.render('Run', True, 'white')
    text_rect = text_image.get_rect(center=run_card.rect.center)
    run_card.image.blit(text_image, text_rect)
    return run_card

def create_text_sprite(font, text, color, padding, align=None, antialias=True, groups=None):
    if groups is None:
        groups = ()
    text_image = font.render(text, antialias, color)
    text_rect = text_image.get_rect()

    size = tuple(a + b for a, b in zip(text_rect.size, padding))
    image = pygame.Surface(size)

    sprite = MonsterSprite(image, *groups)

    alignment = {}
    if align is not None:
        alignment.update({
            align: getattr(sprite.rect, align),
        })
    sprite.image.blit(text_image, text_image.get_rect(**alignment))

    return sprite
