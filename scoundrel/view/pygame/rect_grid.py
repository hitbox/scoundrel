from scoundrel.util import human_split

def int_tuple(iterable):
    return tuple(map(int, iterable))

class RectGrid:

    def __init__(self, tile_size, gap=None, start=None, columnwise=False):
        self.tile_size = tile_size
        self._gap = gap
        self.start = start
        self.columnwise = columnwise

    @classmethod
    def from_config(cls, section):
        tile_size = int_tuple(human_split(section['tile_size']))
        columnwise = section.getboolean('columnwise')
        start = int_tuple(human_split(section.get('start', '0,0')))
        gap = int_tuple(human_split(section.get('gap', '0,0')))
        instance = cls(tile_size=tile_size, gap=gap, start=start, columnwise=columnwise)
        return instance

    @property
    def gap(self):
        return self._gap or (0,0)

    @staticmethod
    def _return_value_func(with_position):
        if with_position:
            def return_value(position, subrect):
                return (position, subrect)
        else:
            def return_value(position, subrect):
                return subrect
        return return_value

    def iter_rects(self, container, with_position=False):
        """
        Generate sub-rects of tile-size from within the image_size rect.
        """
        tile_width, tile_height = self.tile_size
        gap_x, gap_y = self.gap

        return_value = self._return_value_func(with_position)

        y_range = range(container.top, container.bottom, tile_height + gap_y)
        for row, y in enumerate(y_range):
            x_range = range(container.left, container.right, tile_width + gap_x)
            for column, x in enumerate(x_range):
                position = (row, column)
                subrect = (x, y, tile_width, tile_height)
                yield return_value(position, subrect)

    def iter_rects_columnwise(self, container, with_position=False):
        tile_width, tile_height = self.tile_size
        gap_x, gap_y = self.gap

        return_value = self._return_value_func(with_position)

        x_range = range(container.left, container.right, tile_width + gap_x)
        for column, x in enumerate(x_range):
            y_range = range(container.top, container.bottom, tile_height + gap_y)
            for row, y in enumerate(y_range):
                position = (row, column)
                subrect = (x, y, tile_width, tile_height)
                yield return_value(position, subrect)
