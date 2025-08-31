from scoundrel.external import pygame

from . import event_loop
from .quit_prompt import QuitPrompt

class PromptTurn:
    """
    Loop until a card is chosen or a quit event.
    """

    def __init__(self, user_interface, game):
        self.user_interface = user_interface
        self.game = game

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            # Keep running if quit prompt cancelled, otherwise stop.
            return self.user_interface.prompt_for_quit(self.game)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Click to return card for single turn in room.
                card = self.user_interface.get_click_card(event.pos)
                if card:
                    return card

    def update(self, elapsed):
        self.user_interface.update(elapsed, self.game)

    def run(self):
        # Loop until QUIT or card picked from room.
        while True:
            result = event_loop.run(
                self.event_handler,
                self.user_interface.tick,
                self.update,
                self.user_interface.draw,
            )
            if result is not None:
                return result


class PromptQuit:

    def __init__(self, user_interface, game):
        self.user_interface = user_interface
        self.game = game

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            return QuitPrompt.QUIT
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                for sprite in self.user_interface.quit_prompt_sprites:
                    if sprite.rect.collidepoint(event.pos):
                        return sprite.value

    def update(self, elapsed):
        self.user_interface.update(elapsed, self.game)

    def run(self):
        while True:
            result = event_loop.run(
                self.event_handler,
                self.user_interface.tick,
                self.update,
                self.user_interface.draw,
            )
            if result is not None:
                return result
