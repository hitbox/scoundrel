import pygame

from .shape import bounding
from .shape import move_points

class PolygonGroup:

    def __init__(self, polygons):
        self.polygons = polygons

    def move(self, xoffset, yoffset):
        groups = []
        for points in self.polygons:
            groups.append(move_points(points, xoffset, yoffset))
        return groups

    def flat(self):
        for points in self.polygons:
            for point in points:
                yield point

    def bounding(self):
        return bounding(self.flat())

    def bounding_size(self):
        x, y, w, h = self.bounding()
        return (w, h)

    def draw(self, surface, color, width=0):
        for points in self.polygons:
            pygame.draw.polygon(surface, color, points, width)
