from GoState import State
from GoBoard import Board
from GoMove import Move
from GoPoint import Point
import random
EMPTY, BLACK, WHITE = range(0, 3)

class Go:

    def __init__(self, n, path="input.txt"):
        self.size = n
        with open(path, 'r') as f:
            lines = f.readlines()

            self.our_player = int(lines[0])
            self.other_player = 3-self.our_player
            self.cur_step_num = None
            self.good_moves = [Move(Point(1, 1)),
                               Move(Point(1, 2)),
                               Move(Point(1, 3)),
                               Move(Point(2, 1)),
                               Move(Point(2, 3)),
                               Move(Point(3, 1)),
                               Move(Point(3, 2)),
                               Move(Point(3, 3))]

            previous_board_arr = []
            current_board_arr = []
            black_stones = 0
            white_stones = 0

            for line in lines[1: self.size+1]:
                row = [int(x) for x in line.rstrip('\n')]

                previous_board_arr.append(row)

            for line in lines[self.size+1: 2*self.size+1]:
                row = []
                for x in line.rstrip('\n'):
                    row.append(int(x))
                    if int(x) == BLACK:
                        black_stones += 1
                    elif int(x) == WHITE:
                        white_stones += 1
                current_board_arr.append(row)

            previous_board = Board(self.size, previous_board_arr)
            current_board = Board(self.size, current_board_arr)
            self.board = current_board
            self.previous_state = State(previous_board, None, self.other_player, None)
            self.active_state = State(current_board, self.previous_state, self.our_player, None)
            self.set_step_num(black_stones, white_stones)

    def set_step_num(self, num_black_stones, num_white_stones, write_path="helper.txt"):
        if num_black_stones == 0 and num_white_stones == 0 and self.our_player == BLACK:
            with open(write_path, 'w') as f:
                step_num = 1
                f.write(str(step_num))
                self.cur_step_num = step_num
        elif num_black_stones == 1 and num_white_stones == 0 and self.our_player == WHITE:
            with open(write_path, 'w') as f:
                step_num = 2
                f.write(str(step_num))
                self.cur_step_num = step_num
        else:
            with open(write_path, 'r') as f:
                lines = f.readlines()
                self.cur_step_num = 0
                self.cur_step_num = int(lines[0]) + 2
                f.close()
            with open(write_path, 'w') as f:
                f.write(str(self.cur_step_num))


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

    def valid_good_move(self):
        self.good_moves = list(filter(self.board.valid_move_check, self.good_moves))
        return random.choice(self.good_moves)
