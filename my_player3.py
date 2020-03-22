import random
from GO import Go


class RandomBot:

    def __init__(self, N):
        self.size = N
        self.type = 'random'

    def get_legal_moves(self):
        go = Go(self.size)
        legal_moves = go.get_legal_moves()
        return legal_moves

    def print_move(self, move):
        if move.is_play:
            print(str(move.point.x) + ' ' + str(move.point.y))
        else:
            if move.is_pass:
                print('PASS')

    def print_moves(self, legal_moves):
        for move in legal_moves:
            self.print_move(move)

    def select_move(self, legal_moves):
        selected_move = random.choice(legal_moves)
        # self.print_move(selected_move)
        return selected_move

    def write_output(self, move, path="output.txt"):
        res = ""
        if move.is_pass:
            res = "PASS"
        else:
            res += str(move.point.x) + ',' + str(move.point.y)

        with open(path, 'w') as f:
            f.write(res)

if __name__ == "__main__":
    N = 5
    randomBot = RandomBot(N)
    legal_moves = randomBot.get_legal_moves()
    randomBot.print_moves(legal_moves)
    move = randomBot.select_move(legal_moves)
    randomBot.write_output(move)

