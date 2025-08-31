class ChooseMenu:
    """
    Menu to choose from that keeps the position of items.
    """

    def __init__(self, indexed_choices):
        self.indexed_choices = indexed_choices
        self.chosen_indexes = set()
        self.unavailable = set()

    def pick(self, index):
        """
        Add explicitly chosen menu item by index.
        """
        self.chosen_indexes.add(index)

    def is_available(self, index):
        """
        Index is not already chosen or made unavailable.
        """
        return index not in self.chosen_indexes and index not in self.unavailable

    def menu_lines(self):
        """
        Return list of tuples (index, value, label) for current choices.
        """
        menu = []

        for index, value, label in self.indexed_choices:
            if self.is_available(index):
                # Available option
                menu.append((index, value, label))
            else:
                # Blank line index
                menu.append((None, None, label))

        return menu

    def update_for_available(self, available_choices):
        """
        Update current choices, making them unavailable if not in given choices.
        """
        available_values = set(value for value, label in available_choices)
        for index, value, label in self.indexed_choices:
            if value not in available_values:
                self.unavailable.add(index)

    def value_for_index(self, chosen):
        """
        Return value for given index.
        """
        for index, value, _ in self.indexed_choices:
            if index == chosen:
                return value
