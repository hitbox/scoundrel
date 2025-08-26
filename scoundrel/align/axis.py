from enum import Enum

class Axis(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    def get_boundary(self, rect):
        if self == Axis.HORIZONTAL:
            return rect.right
        else:
            return rect.bottom

    def get_boundary_value(self, r1, r2, gap):
        if self == Axis.HORIZONTAL:
            return r1.right + r2.width + gap[0]
        else:
            return r1.bottom + r2.height + gap[1]
