# Các ký hiệu của maze
WALL = '#'
FREE = ' '
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'

class Stone:
    def __init__(self, position, weight):
        self.position = position
        self.weight = weight

    def __eq__(self, other):
        return self.position == other.position and self.weight == other.weight

    def __hash__(self):
        return hash((self.position, self.weight))