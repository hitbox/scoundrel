from operator import attrgetter

from scoundrel.external import pygame

bounds = attrgetter('left', 'top', 'right', 'bottom')

def horizontal(rects, gap_x=0, **kwargs):
    # First rect is not moved.
    for r1, r2 in zip(rects, rects[1:]):
        r2.left = r1.right + gap_x
        for key, value in kwargs.items():
            setattr(r2, key, value)

def vertical(rects, gap_y=0, **kwargs):
    for r1, r2 in zip(rects, rects[1:]):
        r2.top = r1.bottom + gap_y
        for key, value in kwargs.items():
            setattr(r2, key, value)

def bounding(rects):
    """
    Bounding rect of rects
    """
    rects_bounds = map(bounds, rects)
    lefts, tops, rights, bottoms = zip(*rects_bounds)
    left = min(lefts)
    top = min(tops)
    right = max(rights)
    bottom = max(bottoms)
    return (left, top, right - left, bottom - top)

def move_as_group(rects, **kwargs):
    """
    Move rects as one group with pygame.Rect keyword arguments.
    """
    origin = pygame.Rect(bounding(rects))
    moved = pygame.Rect(origin[:])
    for key, value in kwargs.items():
        setattr(moved, key, value)
    dx = moved.x - origin.x
    dy = moved.y - origin.y
    for rect in rects:
        rect.x += dx
        rect.y += dy

def horizontal_wrap(rects, container, gap=None):
    if gap is None:
        gap_x = gap_y = 0
    else:
        gap_x, gap_y = gap
    while True:
        # Rects going off the right side of the container.
        rects = [rect for rect in rects if rect.right > container.right]
        if not rects:
            break
        # Move rects left and order.
        rects[0].left = container.left
        horizontal(rects, gap_x=gap_x)
        bottom = max(rect.bottom for rect in rects)
        for rect in rects:
            rect.top = bottom + gap_y

