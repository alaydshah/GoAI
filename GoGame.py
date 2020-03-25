from GoState import State
from GoBoard import Board
from GoMove import Move
from GoPoint import Point


class Go:

    def __init__(self, n, path="input.txt"):
        self.size = n
        with open(path, 'r') as f:
            lines = f.readlines()

            self.our_player = int(lines[0])
            self.other_player = 3-self.our_player

            previous_board_arr = []
            current_board_arr = []

            for line in lines[1: self.size+1]:
                row = [int(x) for x in line.rstrip('\n')]
                previous_board_arr.append(row)

            for line in lines[self.size+1: 2*self.size+1]:
                row = [int(x) for x in line.rstrip('\n')]
                current_board_arr.append(row)

            previous_board = Board(self.size, previous_board_arr)
            current_board = Board(self.size, current_board_arr)

            self.previous_state = State(previous_board, None, self.other_player, None)
            self.active_state = State(current_board, self.previous_state, self.our_player, None)

    def get_all_moves(self):
        moves = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                point = Point(i, j)
                move = Move(point)
                moves.append(move)
        pass_move = Move()
        moves.append(pass_move)
        return moves
