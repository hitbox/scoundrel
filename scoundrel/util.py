import string

def letter_indexer(iterable):
    """
    Index iterable by letters. Iterable cannot exceed length 26.
    """
    for index, item in enumerate(iterable):
        letter = string.ascii_lowercase[index]
        yield (letter, item)
