from GoPoint import Point
from GoMove import Move

EMPTY, BLACK, WHITE = range(0, 3)


class Board:

    def __init__(self, size, board_arr):
        self.board_size = size
        self.board_grid = board_arr

    def __eq__(self, other):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_grid[i][j] != other.board_grid[i][j]:
                    return False
        return True

    def point_on_grid(self, point: Point):
        return 0 <= point.x < self.board_size and 0 <= point.y < self.board_size

    def coord_is_empty(self, point: Point):
        return self.board_grid[point.x][point.y] == EMPTY

    def get_point_neighbors(self, point):
        return list(filter(self.point_on_grid, point.get_neighbors()))

    def get_neighbor_connections(self, point):
        neighbors = self.get_point_neighbors(point)
        connected_stones = []
        for neighbor_stone in neighbors:
            if self.board_grid[neighbor_stone.x][neighbor_stone.y] == self.board_grid[point.x][point.y]:
                connected_stones.append(neighbor_stone)
        return connected_stones

    def get_connection_chain(self, point):
        stack_stones = [point]
        connection_chain = []
        while stack_stones:
            curr_point = stack_stones.pop()
            connection_chain.append(curr_point)
            neighbor_connections = self.get_neighbor_connections(curr_point)
            for stone in neighbor_connections:
                if stone not in stack_stones and stone not in connection_chain:
                    stack_stones.append(stone)
        return connection_chain

    def has_liberty(self, point):
        connection_chain = self.get_connection_chain(point)
        for stone in connection_chain:
            neighbors = self.get_point_neighbors(stone)
            for neighbor_point in neighbors:
                if self.board_grid[neighbor_point.x][neighbor_point.y] == 0:
                    return True
        return False

    def get_liberty(self, move: Move):
        if move.is_pass:
            return 4
        point = move.point
        liberty = 0
        connection_chain = self.get_connection_chain(point)
        for stone in connection_chain:
            neighbors = self.get_point_neighbors(stone)
            for neighbor_point in neighbors:
                if self.board_grid[neighbor_point.x][neighbor_point.y] == EMPTY:
                    liberty += 1
        return liberty

    def find_adj_dead(self, point):
        dead_stones = set()
        curr_player = self.board_grid[point.x][point.y]
        neighbor_points = self.get_point_neighbors(point)
        for point in neighbor_points:
            if self.board_grid[point.x][point.y] == 3 - curr_player and not self.has_liberty(point):
                connected_chain = self.get_connection_chain(point)
                for stone in connected_chain:
                    dead_stones.add(stone)
        return dead_stones

    def remove_stones(self, set_stones):
        for stone in set_stones:
            self.board_grid[stone.x][stone.y] = EMPTY

    def get_point_color(self, point):
        return self.board_grid[point.x][point.y]

    def place_stone(self, move: Move, player):
        point = move.point
        self.board_grid[point.x][point.y] = player
        dead_stones = self.find_adj_dead(point)
        self.remove_stones(dead_stones)

    def valid_move_check(self, move: Move):
        point = move.point
        return self.point_on_grid(point) and self.coord_is_empty(point)

    def fills_own_eye(self, move: Move):
        if move.is_pass:
            return False
        point = move.point
        player = self.board_grid[point.x][point.y]
        for neighbor in point.get_neighbors():
            if self.point_on_grid(neighbor):
                if self.get_point_color(neighbor) != player:
                    return False
        diagonal_stones = point.get_diagonals()
        opponent_diagonals = 0
        for stone in diagonal_stones:
            if not self.point_on_grid(stone):
                opponent_diagonals += 1
                break
        for stone in diagonal_stones:
            if self.point_on_grid(stone):
                if self.get_point_color(stone) == 3 - player:
                    opponent_diagonals += 1
        if opponent_diagonals > 1:
            return False
        return True

    # def suicidal_move(self, move, player):
    #     point = move.point
    #     self.place_stone(point, player)
    #     return not self.has_liberty(point)

    # def violate_ko(self, other_board):
    #     if self.board_grid == other_board:
    #         return True
