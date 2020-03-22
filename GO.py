from copy import deepcopy
from GoPoint import Point
from GoBoard import Board
from GoMove import Move

class Go:

    def __init__(self, n):
        self.size = n
        self.board = Board(self.size)

    def place_stone(self, move):
        # move = Move(self.board, point)
        # if not move.is_valid_move():
        #     return False
        if not move.isValid:
            return False
        new_board = deepcopy(self.board.current_board)
        new_board[move.point.x][move.point.y] = self.board.player
        self.board.update_board(new_board)
        return True

    def get_legal_moves(self):
        moves = []
        for i in range(0, self.board.board_size):
            for j in range(0, self.board.board_size):
                point = Point(i, j)
                move = Move(self.board, point)
                if move.is_valid_move():
                    moves.append(move)

        pass_move = Move(self.board, None)
        moves.append(pass_move)
        return moves

    def is_point_eye(self, point:Point):

        if not self.board.coord_is_empty(point):
            return False

        if not self.board.point_on_grid(point):
            return False

        for neighbor in point.get_neighbors():
            if self.board.point_on_grid(neighbor):
                if self.board.get_point_color(neighbor) != self.board.player:
                    return False

        diag_stones = point.get_diagonals()
        opp_diags = 0

        for stone in diag_stones:
            if not self.board.point_on_grid(stone):
                opp_diags += 1
                break

        for stone in diag_stones:
            if self.board.get_point_color(stone) == 3-self.board.player:
                opp_diags += 1

        if opp_diags > 1:
            return False

        return True
