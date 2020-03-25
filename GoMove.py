class Move:

    def __init__(self, point=None):
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = not self.is_play
        assert self.is_play ^ self.is_pass

    @classmethod
    def play(cls, point):
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        return Move()

    def __str__(self):
        if self.is_play:
            return str(self.point.x) + ',' + str(self.point.y)
        else:
            return "PASS\n"
