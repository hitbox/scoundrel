from scoundrel.external import pygame

def strip_alpha(surface):
    rect = surface.get_bounding_rect()
    if rect.width == 0 or rect.height == 0:
        return None
    return surface.subsurface(rect).copy()

def post_quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))

def scaleby(image, scalar):
    width, height = map(lambda d: d * scalar, image.get_size())
    return pygame.transform.scale(image, (width, height))

def create_sprite_from_card(card, image, rect=None, deck=None):
    if rect is None:
        rect = image.get_rect()
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = rect
    sprite.card = card
    sprite.deck = deck
    return sprite
