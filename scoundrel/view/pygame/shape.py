import contextlib
import math
import operator
import os

from itertools import chain

with contextlib.redirect_stdout(open(os.devnull, 'w')):
    import pygame

def rect_from_size(size):
    return pygame.Rect((0,0), size)

def move_attr(rect, **kwargs):
    if not kwargs:
        raise RuntimeError('No keyword arguments.')

    rect = rect.copy()
    for key, value in kwargs.items():
        setattr(rect, key, value)
    return rect

def cwpoints(rect):
    yield rect.topleft
    yield rect.topright
    yield rect.bottomright
    yield rect.bottomleft

def move_points(points, x, y):
    return [(px + x, py + y) for px, py in points]

def mirrorx(points, centerx):
    return [(2*centerx - x, y) for x, y in points]

def bounding(points):
    xs, ys = zip(*points)
    left = min(xs)
    top = min(ys)
    right = max(xs)
    bottom = max(ys)
    return (left, top, right - left, bottom - top)

def angle_between(p1, p2):
    # screen space
    return math.atan2(p2[1] + p1[1], p2[0] - p1[0])

def normalize_to_origin(points):
    xs, ys = zip(*points)
    minx = min(xs)
    miny = min(ys)

    result = []
    for x, y in points:
        if minx < 0:
            x += abs(minx)
        if miny < 0:
            y += abs(miny)
        result.append((x,y))
    return result

def create_heart_points(size):
    rect = rect_from_size(size)

    step = 15
    start_point = (rect.centerx, rect.height / 10)
    center = (3 * rect.width / 4, rect.height / 4)
    assert start_point[0] < center[0]

    right_side = [start_point]

    radius = math.dist(start_point, center)

    arc = int(math.degrees(angle_between(center, start_point)))
    arc = range(arc, 0, -step)
    angles = list(map(math.radians, arc))
    right_side.extend(create_circle_points(radius, center, angles))

    angles = list(map(math.radians, reversed(range(315, 360, step))))
    right_side.extend(create_circle_points(radius, center, angles))

    right_side.append(rect.midbottom)

    # mirror right side excluding shared points
    left_side = mirrorx(right_side[1:-1], rect.centerx)

    # reverse left_side so that points are ordered correctly
    joined = right_side + left_side[::-1]
    points = [(int(x), int(y)) for x, y in joined]
    
    points = normalize_to_origin(points)

    return points

def create_diamond_points(size):
    rect = rect_from_size(size)
    return (rect.midtop, rect.midright, rect.midbottom, rect.midleft)

def create_circle_points(radius, center, angles):
    centerx, centery = center
    for angle in angles:
        x = centerx + math.cos(angle) * radius
        y = centery - math.sin(angle) * radius
        yield (x, y)

def create_club_points_groups(size):
    width, height = size
    rect = rect_from_size(size)

    points = []
    step = 15
    radius = 7 * width / 32
    center = (rect.centerx, radius)

    # Top lobe
    arc1 = range(240, 0, -step)
    arc2 = reversed(range(300, 360, step))
    angles = map(math.radians, chain(arc1, arc2))
    points.extend(create_circle_points(radius, center, angles))

    # Right lobe
    last_x, last_y = points[-1]
    centerx = last_x + math.cos(math.radians(300)) * radius
    centery = last_y + -math.sin(math.radians(300)) * radius
    arc1 = range(135, 0, -step)
    arc2 = reversed(range(225, 360, step))
    angles = map(math.radians, chain(arc1, arc2))
    points.extend(create_circle_points(radius, (centerx, centery), angles))

    # Stem
    last_x, last_y = points[-1]
    points.extend([
        (last_x, rect.bottom),
        (rect.centerx - (last_x - rect.centerx), rect.bottom),
        (rect.centerx - (last_x - rect.centerx), last_y),
    ])

    # Left lobe
    last_x, last_y = points[-1]
    center = (
        last_x + math.cos(math.radians(135)) * radius,
        last_y - math.sin(math.radians(135)) * radius,
    )
    arc1 = reversed(range(45, 315, step))
    angles = map(math.radians, chain(arc1))
    points.extend(create_circle_points(radius, center, angles))

    points = normalize_to_origin(points)

    return [points]

def create_spade_points_groups(size):
    rect = rect_from_size(size)

    right_side = [
        rect.midtop,
        rect.midright,
        (rect.right, 2 * rect.height / 3),
        (rect.centerx + rect.width * 0.05, 2 * rect.height / 3),
        (rect.centerx + rect.width * 0.05, rect.bottom),
        rect.midbottom,
    ]

    left_side = mirrorx(right_side[1:-1], rect.centerx)
    joined = right_side + left_side[::-1]
    joined = [(int(x), int(y)) for x, y in joined]

    return [joined]
