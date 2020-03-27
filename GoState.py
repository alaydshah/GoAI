from GoBoard import Board
from GoMove import Move
from GoPoint import Point
from copy import deepcopy

EMPTY, BLACK, WHITE = range(0, 3)


class State:

    def __init__(self, board, p_state, next_player, move):
        self.board: Board = board
        self.previous_state: State = p_state
        self.next_player = next_player
        self.other_player = 3 - next_player
        self.last_move: Move = move

    # def is_move_valid(self, move):
    #     if move.is_pass:
    #         return True
    #     if not self.board.valid_point_check(move):
    #         return False
    #     temp_board = deepcopy(self.board)
    #     temp_board.place_stone(move, self.next_player)
    #     if not temp_board.has_liberty(move.point):
    #         return False
    #     if temp_board == self.previous_state.board:
    #         return False
    #     return True

    def apply_move(self, move: Move):
        next_board = deepcopy(self.board)
        if move.is_play:
            if not self.board.valid_move_check(move):  # Basic Move Validity Checks
                return None
            next_board.place_stone(move, self.next_player)
            point: Point = move.point
            if not next_board.has_liberty(point):  # Suicidal Move Check
                return None
            if next_board == self.previous_state.board:  # Ko Violation check
                return None
        return State(next_board, self, self.other_player, move)



    def stone_diff(self):
        black_stones = 0
        white_stones = 0
        for i in range(self.board.board_size):
            for j in range(self.board.board_size):
                point = Point(i, j)
                if self.board.get_point_color(point) == BLACK:
                    black_stones += 1
                elif self.board.get_point_color(point) == WHITE:
                    white_stones += 1
        return black_stones - white_stones - self.board.board_size/2.0

    def is_terminal(self):
        last_move: Move = self.last_move
        last_to_last_move: Move = self.previous_state.last_move
        if last_move is not None and last_to_last_move is not None:
            return last_move.is_pass and last_to_last_move.is_pass
        return False




