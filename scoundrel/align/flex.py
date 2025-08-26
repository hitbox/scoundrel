import operator

from scoundrel.external import pygame

from .axis import Axis
from .direction import Direction

class FlexLayout:

    def __init__(self, origin, axis, direction, boundary, gap=None):
        self.origin = origin
        self.axis = Axis(axis)
        self.direction = Direction(direction)
        self.boundary = boundary
        if gap is None:
            gap = (0, 0)
        self.gap = gap

    @property
    def gap_x(self):
        # XXX: Dependency for AlignmentAttributes
        return self.gap[0]

    @property
    def gap_y(self):
        # XXX: Dependency for AlignmentAttributes
        return self.gap[1]

    @classmethod
    def from_rect(cls, container, axis, direction, gap=None):
        boundary = Axis(axis).get_boundary(container)
        if direction == Direction.FORWARD:
            origin = container.topleft
        else:
            origin = container.bottomleft
        return cls(origin, axis, direction, boundary, gap)

    @classmethod
    def from_columns(cls, tile_width, ncols, direction=None, gap=None, **kwargs):
        if direction is None:
            direction = Direction.FORWARD
        direction = Direction(direction)

        if gap is None:
            gap = (0, 0)
        gap_x, gap_y = gap

        container = pygame.Rect(0, 0, (tile_width + gap_x) * ncols, 0)
        for key, value in kwargs.items():
            setattr(container, key, value)
        return cls.from_rect(container, Axis.HORIZONTAL, direction, gap=gap)

    @classmethod
    def from_rows(cls, tile_height, nrows, direction=None, gap=None, **kwargs):
        if direction is None:
            direction = Direction.FORWARD
        direction = Direction(direction)

        if gap is None:
            gap = (0, 0)
        gap_x, gap_y = gap

        container = pygame.Rect(0, 0, 0, (tile_height + gap_y) * nrows)
        for key, value in kwargs.items():
            setattr(container, key, value)
        return cls.from_rect(container, Axis.VERTICAL, direction, gap=gap)

    def update_for_direction(self, rect1, rect2):
        if Axis(self.axis) == Axis.HORIZONTAL:
            rect2.left = rect1.right + self.gap[0]
            rect2.top = rect1.top
        else:
            rect2.top = rect1.bottom + self.gap[1]
            rect2.left = rect1.left

    def _get_anchor_and_rects(self, rects, sizes):
        """
        Return the first rect and the list of rects. If the first rect is None,
        also create a new list with a new rect so that pairwise operations
        work.
        """
        anchor = rects[0]
        if anchor is None:
            anchor = pygame.Rect(self.origin, sizes[0])
            rects = [anchor] + rects[1:]

        if self.direction == Direction.FORWARD:
            anchor.topleft = self.origin
        else:
            anchor.bottomleft = self.origin

        return (anchor, rects)

    def __call__(self, rects):
        """
        Layout rects wrapping inside this container horizontally. Allows None
        in rect list for empty slots.
        """
        sizes = [rect.size for rect in rects if rect is not None]
        if not sizes:
            # Nothing to do, empty list or all rects are None.
            return

        anchor, rects = self._get_anchor_and_rects(rects, sizes)
        gap_x, gap_y = self.gap

        direction = Direction(self.direction)
        paired_rects = zip(rects, rects[1:])

        boundary_op = operator.gt if direction == Direction.FORWARD else operator.lt

        axis = Axis(self.axis)
        for r1, r2 in paired_rects:
            # Skip pair for either is None.
            if r1 is None or r2 is None:
                continue

            if self.boundary is None:
                needs_wrap = False
            else:
                needs_wrap = boundary_op(
                    axis.get_boundary_value(r1, r2, self.gap),
                    self.boundary,
                )
            if needs_wrap:
                # Wrap to anchor for boundary.
                if axis == Axis.HORIZONTAL:
                    if direction == Direction.FORWARD:
                        # horizontal left-to-right wrap to newline
                        r2.topleft = (anchor.left, anchor.bottom + gap_y)
                    else:
                        # horizontal right-to-left wrap to newline
                        r2.topright = (anchor.right, anchor.bottom + gap_y)
                else:
                    if direction == Direction.REVERSE:
                        # vertical bottom-to-top
                        r2.topleft = (anchor.right + gap_x, anchor.top)
                    else:
                        # vertical top-to-bottom
                        r2.bottomleft = (anchor.right + gap_x, anchor.bottom)
                anchor = r2
            else:
                # No wrap, normal flow.
                alignment_attributes = alignment_attr_map[(axis, direction)]
                alignment_attributes.update_with_gap(r1, r2, self)
                alignment_attributes.update_no_gap(r1, r2)


class AlignmentAttributes:

    def __init__(self, with_gap_attrs, no_gap_attrs):
        self.with_gap_attrs = with_gap_attrs
        self.no_gap_attrs = no_gap_attrs

    def update_with_gap(self, r1, r2, gap_obj):
        target, source, gap_attr = self.with_gap_attrs
        gap = getattr(gap_obj, gap_attr)
        if gap_obj.direction == Direction.REVERSE:
            gap = -gap
        setattr(r2, target, getattr(r1, source) + gap)

    def update_no_gap(self, r1, r2):
        target, source = self.no_gap_attrs
        setattr(r2, target, getattr(r1, source))


alignment_attr_map = {
    # (attr_tuple_with_gap, attr_tuple_without_gap)
    (Axis.HORIZONTAL, Direction.FORWARD): AlignmentAttributes(
        with_gap_attrs = ('left', 'right', 'gap_x'),
        no_gap_attrs = ('top', 'top'),
    ),
    (Axis.HORIZONTAL, Direction.REVERSE): AlignmentAttributes(
        with_gap_attrs = ('right', 'left', 'gap_x'),
        no_gap_attrs = ('top', 'top'),
    ),
    (Axis.VERTICAL, Direction.FORWARD): AlignmentAttributes(
        with_gap_attrs = ('top', 'bottom', 'gap_y'),
        no_gap_attrs = ('left', 'left'),
    ),
    (Axis.VERTICAL, Direction.REVERSE): AlignmentAttributes(
        with_gap_attrs = ('bottom', 'top', 'gap_y'),
        no_gap_attrs = ('left', 'left'),
    ),
}
