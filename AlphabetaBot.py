from GoGame import Go
from GoPoint import Point
from GoMove import Move
from GoState import State
from random import shuffle
from copy import deepcopy
import random
EMPTY, BLACK, WHITE = range(0, 3)

MAX_SCORE = 999999
MIN_SCORE = -999999

class AlphabetaBot:

    def __init__(self, size, depth):
        self.size = size
        self.type = 'AlphaBeta'
        self.all_moves = None
        self.our_player = None
        self.depth = depth
        self.step_num = None

    def max_value(self, state: State, depth, alpha, beta):
        if state.is_terminal():
            return self.utility_function(state)
        if depth == 0:
            return self.eval_function(state)
        best_recorded_score = MIN_SCORE
        moves = deepcopy(self.all_moves)
        shuffle(moves)
        for move in moves:
            new_state = state.apply_move(move)
            if new_state is not None:
                if not new_state.board.fills_own_eye(move):
                    cur_move_score = self.min_value(new_state, depth-1, alpha, beta)
                    if cur_move_score > best_recorded_score:
                        best_recorded_score = cur_move_score
                        alpha = max(alpha, best_recorded_score)
                        if beta <= alpha:
                            return best_recorded_score
        return best_recorded_score

    def min_value(self, state:State, depth, alpha, beta):
        if state.is_terminal():
            self.utility_function(state)
        if depth == 0:
            return self.eval_function(state)
        least_recorded_score = MAX_SCORE
        moves = deepcopy(self.all_moves)
        shuffle(moves)
        for move in moves:
            new_state = state.apply_move(move)
            if new_state is not None:
                if not new_state.board.fills_own_eye(move):
                    cur_move_score = self.max_value(new_state, depth-1, alpha, beta)
                    if cur_move_score < least_recorded_score:
                        least_recorded_score = cur_move_score
                        beta = min(beta, least_recorded_score)
                        if beta <= alpha:
                            return least_recorded_score
        return least_recorded_score

    def select_move(self):
        go = Go(self.size)
        self.all_moves = go.get_all_moves()
        self.our_player = go.our_player
        self.step_num = go.cur_step_num
        self.depth = min(self.depth, 24-self.step_num)
        if self.step_num < 7:
            return go.valid_good_move()

        moves = deepcopy(self.all_moves)
        shuffle(moves)
        best_moves_list = []
        alpha = MIN_SCORE
        beta = MAX_SCORE
        best_recorded_score = MIN_SCORE
        if self.depth < 0:
            for move in moves:
                new_state = go.active_state.apply_move(move)
                if new_state is not None:
                    if not new_state.board.fills_own_eye(move):
                        best_moves_list.append(move)
        else:
            for move in moves:
                new_state = go.active_state.apply_move(move)
                if new_state is not None:
                    if not new_state.board.fills_own_eye(move):
                        cur_move_score = self.min_value(new_state, self.depth, alpha, beta)
                        if cur_move_score == best_recorded_score:
                            best_moves_list.append(move)
                        if cur_move_score > best_recorded_score:
                            best_moves_list = [move]
                            best_recorded_score = cur_move_score
            if not best_moves_list:
                best_moves_list.append(Move())
        return random.choice(best_moves_list)

    def eval_function(self, state: State):
        black_minus_white = state.stone_diff()
        if self.our_player == WHITE:
            return -1 * black_minus_white
        return black_minus_white

    def utility_function(self, state: State):
        if state.winner() == self.our_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    @staticmethod
    def write_output(move, path="output.txt"):
        cur_move: Move = move
        result = ""
        result += str(cur_move)
        with open(path, 'w') as f:
            f.write(result)


if __name__ == "__main__":
    N = 5
    depth = 3
    alphabetaBot = AlphabetaBot(N, depth)
    selected_move = alphabetaBot.select_move()
    alphabetaBot.write_output(selected_move)