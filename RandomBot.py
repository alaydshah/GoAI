import random
from GoGame import Go
from GoMove import Move


class RandomBot:

    def __init__(self, size):
        self.size = size
        self.type = 'random'

    def get_legal_moves(self):
        legal_moves = []
        go = Go(self.size)
        all_moves = go.get_all_moves()
        for move in all_moves:
            state = go.active_state.apply_move(move)
            if state is not None:
                legal_moves.append(move)
        return legal_moves

    @staticmethod
    def select_move(legal_moves):
        move = random.choice(legal_moves)
        return move

    @staticmethod
    def print_moves(legal_moves):
        for move in legal_moves:
            print(move)

    @staticmethod
    def write_output(move, path="output.txt"):
        cur_move: Move = move
        result = ""
        result += str(cur_move)
        with open(path, 'w') as f:
            f.write(result)


if __name__ == "__main__":
    N = 5
    randomBot = RandomBot(N)
    legit_moves = randomBot.get_legal_moves()
    randomBot.print_moves(legit_moves)
    selected_move = randomBot.select_move(legit_moves)
    randomBot.write_output(selected_move)
