from copy import deepcopy

EMPTY, BLACK, WHITE = range(0,3)

class Board:

    def __init__(self, n, path="input.txt"):

        self.board_size = n

        with open(path, 'r') as f:
            lines = f.readlines()

            self.player = int(lines[0])

            self.previous_board = []
            self.current_board = []

            for line in lines[1:self.board_size+1]:
                # self.previous_board = [].append([int(x) for x in line.rstrip('\n')])
                row = [int(x) for x in line.rstrip('\n')]
                self.previous_board.append(row)

            for line in lines[self.board_size+1 : 2*self.board_size+1]:
                # self.current_board = [].append([int(x) for x in line.rstrip('\n')])
                row = [int(x) for x in line.rstrip('\n')]
                self.current_board.append(row)

    def update_board(self, new_board):
        self.previous_board = deepcopy(self.current_board)
        self.current_board = new_board

    def compare_board(self, board_1, board_2):
        for i in range(self.board_size):
            for j  in range(self.board_size):
                if board_1[i][j] == board_2[i][j]:
                    return False
        return True

    def point_on_grid(self, point):
        return 0 <= point.x < self.board_size and 0 <= point.y < self.board_size

    def coord_is_empty(self, point):
        return self.current_board[point.x][point.y] == 0

    def get_point_neighbors(self, point):
        return list(filter(self.point_on_grid, point.get_neighbors()))

    def get_neighbor_connections(self, point):
        neighbors = self.get_point_neighbors(point)
        connected_stones = []
        for neighbor_stone in neighbors:
            if self.current_board[neighbor_stone.x][neighbor_stone.y] == self.current_board[point.x][point.y]:
                connected_stones.append(neighbor_stone)
        return connected_stones

    def connections_dfs(self, point):
        stack = [point]
        connected_stones = []
        while stack:
            curr_point = stack.pop()
            connected_stones.append(curr_point)
            neighbor_connections = self.get_neighbor_connections(curr_point)
            for stone in neighbor_connections:
                if stone not in stack and stone not in connected_stones:
                    stack.append(stone)
        return connected_stones

    def has_liberty(self, point):
        connected_stones = self.connections_dfs(point)
        for stone in connected_stones:
            neighbors = self.get_point_neighbors(stone)
            for neighbor_point in neighbors:
                if self.current_board[neighbor_point.x][neighbor_point.y] == 0:
                    return True
        return False

    def find_adj_dead(self, point):
        dead_stones = set()
        neighbor_stones = self.get_point_neighbors(point)
        for stone in neighbor_stones:
            if self.current_board[stone.x][stone.y] == 3-self.player and not self.has_liberty(stone):
                connected_group = self.connections_dfs(stone)
                for piece in connected_group:
                    dead_stones.add(piece)
        return dead_stones

    def remove_stones(self, set_stones):
        clean_board = deepcopy(self.current_board)
        for stone in set_stones:
            clean_board[stone.x][stone.y] = 0
        self.update_board(clean_board)

    def get_point_color(self, point):
        return self.current_board[point.x][point.y]
