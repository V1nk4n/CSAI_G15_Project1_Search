from queue import PriorityQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone


class Node:
    def __init__(self, maze, ares, stones, switches, g = 0, prev_state=None):
        self.maze = [row[:] for row in maze]
        self.ares = ares
        self.stones = stones
        self.switches = switches
        self.cost = g
        self.prev_state = prev_state

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.ares == other.ares and
                self.stones == other.stones and
                self.switches == other.switches)

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash((self.ares, tuple(self.stones), tuple(self.switches)))

    def is_goal(self):
        return all(stone.position in self.switches for stone in self.stones)

    def get_state(self, move):
        x, y = self.ares
        new_x, new_y = x + move[0], y + move[1]
        width, height = len(self.maze), len(self.maze[0])

        if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
            return None

        if self.maze[new_x][new_y] == WALL:
            return None

        new_stones = list(self.stones)
        new_maze = [row[:] for row in self.maze]
        new_ares = (new_x, new_y)

        for i_stone, stone in enumerate(self.stones):
            if (new_x, new_y) == stone.position:
                new_x_stone, new_y_stone = new_x + move[0], new_y + move[1]
                if (0 <= new_x_stone < width and 0 <= new_y_stone < height and
                        new_maze[new_x_stone][new_y_stone] in (FREE, SWITCH)):

                    new_stone = Stone((new_x_stone, new_y_stone), stone.weight)
                    new_stones[i_stone] = new_stone

                    new_maze[new_x_stone][new_y_stone] = STONE_ON_SWITCH if new_maze[new_x_stone][new_y_stone] == SWITCH else STONE
                    new_maze[x][y] = SWITCH if (
                        x, y) in self.switches else FREE
                    new_maze[new_x][new_y] = ARES_ON_SWITCH if new_maze[new_x][new_y] == SWITCH else ARES

                    new_cost = self.cost + 1 + new_stone.weight

                    return Node(new_maze, new_ares, new_stones, self.switches, new_cost, self)

        if self.maze[new_x][new_y] in (STONE, STONE_ON_SWITCH):
            return None

        new_maze[x][y] = SWITCH if (x, y) in self.switches else FREE
        new_maze[new_x][new_y] = ARES_ON_SWITCH if new_maze[new_x][new_y] == SWITCH else ARES
        return Node(new_maze, new_ares, new_stones, self.switches, self.cost + 1, self)

    def stone_in_corner(self):
        for stone in self.stones:
            if stone.position not in self.switches:
                x, y = stone.position
                if (self.maze[x-1][y] == WALL or self.maze[x+1][y] == WALL) and (self.maze[x][y-1] == WALL or self.maze[x][y+1] == WALL):
                    return True
        return False

    def get_neighbors(self):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        neighbors = []
        for move in moves:
            # Chỉ gọi get_state khi bước di chuyển hợp lệ
            next_state = self.get_state(move)
            if next_state and not next_state.stone_in_corner():
                neighbors.append(next_state)
        return neighbors
