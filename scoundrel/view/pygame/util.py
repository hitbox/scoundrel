def strip_alpha(surface):
    rect = surface.get_bounding_rect()
    if rect.width == 0 or rect.height == 0:
        return None
    return surface.subsurface(rect).copy()
