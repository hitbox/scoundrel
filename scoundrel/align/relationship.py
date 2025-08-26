class RelationshipManager:

    def __init__(self):
        self.relationships = []


class AlignRelationship:

    def __init__(self, to_index, from_attr, to_attr):
        self.to_index = to_index
        self.from_attr = from_attr # attribute to set
        self.to_attr = to_attr # attribute to get value

    def __call__(self, *items):
        align_to = items[self.to_index]
        value = getattr(align_to, self.to_attr)
        for from_item in items:
            if from_item is not align_to:
                setattr(from_item, self.from_attr, value)
