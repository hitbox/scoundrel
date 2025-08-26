class Relationship:

    def __init__(self, sprite1, sprite2, func):
        self.sprite1 = sprite1
        self.sprite2 = sprite2
        self.func = func

    def update(self):
        return self.func(self.sprite1, self.sprite2)


class RelationshipManager:

    def __init__(self):
        self.relationships = []

    def append(self, relationship):
        self.relationships.append(relationship)

    def update(self):
        for relationship in self.relationships:
            relationship.update()
