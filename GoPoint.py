class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def neighbors(self):
    #     return [Point(x, y): list(filter(_check_bounds, [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]))]

    def get_neighbors(self):
        return [Point(self.x-1, self.y),
                Point(self.x+1, self.y),
                Point(self.x, self.y-1),
                Point(self.x, self.y+1)]

    def get_diagonals(self):
        return [Point(self.x-1, self.y-1),
                Point(self.x+1, self.y+1),
                Point(self.x+1, self.y-1),
                Point(self.x-1, self.y+1)]

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))
