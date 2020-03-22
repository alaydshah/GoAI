from copy import deepcopy
from GoBoard import Board

class Move:

    def __init__(self, board, point=None):
        self.board = board
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = not self.is_play
        self.isValid = self.is_pass


    def pass_turn(self):
        self.is_play = False
        self.is_pass = True
        self.isValid = True
        self.point = None

    def is_valid_move(self):

        # BASIC CHECKS
        if self.is_pass:
            return True

        if not self.board.point_on_grid(self.point):
            return False

        if not self.board.coord_is_empty(self.point):
            return False

        # Simulating the move in temp_board
        temp_board:Board = deepcopy(self.board)
        temp_board.current_board[self.point.x][self.point.y] = self.board.player

        # Removing the stones adjacent to the point if any after simulating the move
        dead_stones = temp_board.find_adj_dead(self.point)
        temp_board.remove_stones(dead_stones)

        # Verifying is move is not suicidal
        if not temp_board.has_liberty(self.point):
            return False

        #Verifying if move is not KO
        if temp_board.compare_board(self.board.previous_board, temp_board.current_board):
            return False

        self.isValid = True
        return self.isValid


