from scoundrel.external import pygame

def run(event_handler, tick, update, draw):
    """
    pygame loop until event_handler returns anything but None.
    """
    while True:
        for event in pygame.event.get():
            result = event_handler(event)
            if result is not None:
                return result

        elapsed = tick()
        update(elapsed)
        draw()
        pygame.display.update()
