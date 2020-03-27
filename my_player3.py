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
MAX_T_SCORE = 99999
MIN_T_SCORE = -99999

class AlphabetaBot:

    def __init__(self, size):
        self.size = size
        self.type = 'AlphaBeta'
        self.all_moves = None
        self.our_player = None
        self.depth = None
        self.step_num = None
        self.remaining_steps = None
        self.center_moves_set = (Move(Point(1, 1)),
                                 Move(Point(1, 2)),
                                 Move(Point(1, 3)),
                                 Move(Point(2, 1)),
                                 Move(Point(2, 2)),
                                 Move(Point(2, 3)),
                                 Move(Point(3, 1)),
                                 Move(Point(3, 2)),
                                 Move(Point(3, 3)))

    def max_value(self, state: State, depth, alpha, beta):
        if state.is_terminal() or self.remaining_steps - depth == 0:
            return self.utility_function(state)
        if depth == self.depth:
            return self.eval_function(state)
        best_recorded_score = MIN_SCORE
        moves = deepcopy(self.all_moves)
        shuffle(moves)
        for move in moves:
            new_state = state.apply_move(move)
            if new_state is not None:
                cur_move_score = self.min_value(new_state, depth+1, alpha, beta)
                if cur_move_score > best_recorded_score:
                    best_recorded_score = cur_move_score
                    alpha = max(alpha, best_recorded_score)
                    if beta <= alpha:
                        return best_recorded_score
        return best_recorded_score

    def min_value(self, state: State, depth, alpha, beta):
        if state.is_terminal() or self.remaining_steps - depth == 0:
            return self.utility_function(state)
        if depth == self.depth:
            return self.eval_function(state)
        least_recorded_score = MAX_SCORE
        moves = deepcopy(self.all_moves)
        shuffle(moves)
        for move in moves:
            new_state = state.apply_move(move)
            if new_state is not None:
                cur_move_score = self.max_value(new_state, depth+1, alpha, beta)
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
        if self.step_num < 5:
            move = go.valid_good_move()
            if isinstance(move, Move):
                return move
        elif self.step_num < 9:
            self.depth = 2
        elif self.step_num < 15:
            self.depth = 3
        else:
            self.depth = 4
        self.remaining_steps = 24 - self.step_num
        moves = deepcopy(self.all_moves)
        shuffle(moves)
        best_moves_set = set()
        alpha = MIN_SCORE
        beta = MAX_SCORE
        best_recorded_score = MIN_SCORE

        for move in moves:
            new_state = go.active_state.apply_move(move)
            if new_state is not None:
                    cur_move_score = self.min_value(new_state, 0, alpha, beta)
                    if cur_move_score == best_recorded_score:
                        best_moves_set.add(move)
                    if cur_move_score > best_recorded_score:
                        best_moves_set = set()
                        best_moves_set.add(move)
                        best_recorded_score = cur_move_score
        priority_moves_set = best_moves_set.intersection(self.center_moves_set)
        if priority_moves_set:
            return random.choice(list(priority_moves_set))
        elif best_moves_set:
            return random.choice(list(best_moves_set))
        else:
            return Move()


    def eval_function(self, state: State):
        black_minus_white = state.stone_diff()
        if self.our_player == WHITE:
            return -1 * black_minus_white
        return black_minus_white

    def utility_function(self, state: State):
        eval_value = self.eval_function(state)
        if eval_value > 0:
            return MAX_T_SCORE + eval_value
        else:
            return MIN_T_SCORE + eval_value

    @staticmethod
    def write_output(move, path="output.txt"):
        cur_move: Move = move
        result = ""
        result += str(cur_move)
        with open(path, 'w') as f:
            f.write(result)


if __name__ == "__main__":
    N = 5
    alphabetaBot = AlphabetaBot(N)
    selected_move = alphabetaBot.select_move()
    alphabetaBot.write_output(selected_move)
