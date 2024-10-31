from queue import PriorityQueue
import time
import psutil
import tracemalloc

WALL = '#'
FREE = ' '
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'

NODES = 0

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) # Tính khoảng cách Manhattan giữa 2 điểm

class Stone:
    def __init__(self, position, weight):
        self.position = position
        self.weight = weight

    def __eq__(self, other):
        return self.position == other.position and self.weight == other.weight

    def __hash__(self):
        return hash((self.position, self.weight))

class State:
    def __init__(self, maze, ares, stones, switches, g=0, prev_state=None):
        self.maze = [row[:] for row in maze]
        self.ares = ares
        self.stones = stones
        self.switches = switches
        self.g = g  # Cost to reach this state
        self.cost = self.g
        self.prev_state = prev_state

    def __eq__(self, other):
        if not isinstance(other, State):
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
        x, y = self.ares[0], self.ares[1]
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

                    new_state = State(
                        new_maze, new_ares, new_stones, self.switches, self.g + 1, self)

                    return new_state

        if new_maze[new_x][new_y] == STONE or new_maze[new_x][new_y] == STONE_ON_SWITCH:
            return None

        new_maze[x][y] = SWITCH if (x, y) in self.switches else FREE
        new_maze[new_x][new_y] = ARES_ON_SWITCH if new_maze[new_x][new_y] == SWITCH else ARES
        new_state = State(new_maze, new_ares, new_stones,
                          self.switches, self.g + 1, self)
        return new_state

    def get_neighbors(self):
        neighbors = []
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in moves:
            new_state = self.get_state(move)
            if new_state is not None:
                neighbors.append(new_state)

        return neighbors

def uniform_cost_search(maze, ares_start, stones, switches):
    global NODES
    frontier = PriorityQueue()  # Priority queue based on cost
    expanded = set()  # Explored states
    frontier_set = set()  # For quick check if a state is in frontier

    initial_state = State(maze, ares_start, stones, switches)
    frontier.put((initial_state.cost, initial_state))
    frontier_set.add(initial_state)
    NODES += 1

    while not frontier.empty():
        _, current_state = frontier.get()
        frontier_set.remove(current_state)

        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1]

        expanded.add(current_state)

        neighbors = current_state.get_neighbors()
        for neighbor in neighbors:
            if neighbor in expanded:
                continue

            if neighbor not in frontier_set:
                frontier.put((neighbor.cost, neighbor))
                frontier_set.add(neighbor)
                NODES += 1

    return None

def load_map(path):
    with open(path, 'r') as file:
        first_line = file.readline().strip()
        weights = list(map(int, first_line.split()))
        maze = [list(line.strip()) for line in file.readlines()]

    i_stone = 0
    stones = []
    switches = []

    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == '@' or col == '+':
                ares_start = (i, j)
            elif col == '$' or col == '*':
                stone_position = (i, j)
                stone_weight = weights[i_stone]
                stone = Stone(stone_position, stone_weight)
                stones.append(stone)
                i_stone += 1
            elif col == '.':
                switches.append((i, j))

    return maze, ares_start, stones, switches

def get_move(prev_ares, curr_ares, stone_move):
    dx, dy = curr_ares[0] - prev_ares[0], curr_ares[1] - prev_ares[1]
    action = ''

    if dx == 0 and dy == -1:  # Di chuyển sang trái
        action = 'l' if not stone_move else 'L'
    elif dx == 0 and dy == 1:  # Di chuyển sang phải
        action = 'r' if not stone_move else 'R'
    elif dx == -1 and dy == 0:  # Di chuyển lên
        action = 'u' if not stone_move else 'U'
    elif dx == 1 and dy == 0:  # Di chuyển xuống
        action = 'd' if not stone_move else 'D'

    return action

def visualize(path):
    for state in path:
        for i, row in enumerate(state.maze):
            for j, col in enumerate(row):
                if (i, j) == state.ares:
                    print(ARES, end=' ')
                elif (i, j) in [stone.position for stone in state.stones]:
                    print(STONE, end=' ')
                elif col == SWITCH:
                    print(SWITCH, end=' ')
                else:
                    print(col, end=' ')
            print()
        print("--------------")
        time.sleep(1)

if __name__ == '__main__':
    maze_txt = r'C:\Users\LENOVO\Downloads\Lab01_Search\test.txt'
    maze, ares_start, stones, switches = load_map(maze_txt)
    tracemalloc.start()
    start_time = time.time()
    path = uniform_cost_search(maze, ares_start, stones, switches)
    end_time = time.time()
    current_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed_time = (end_time - start_time) * 1000
    memory_usage = current_memory / (1024 * 1024)

    actions = []
    total_steps = 0
    total_weight = 0

    for current in path[1:]:
        current_state = current
        prev_state = current.prev_state
        stone_move = 0
        for (current_stone, prev_stone) in zip(current_state.stones, prev_state.stones):
            if current_stone != prev_stone:
                total_weight += current_stone.weight
                stone_move = 1
                break

        move = get_move(prev_state.ares, current_state.ares, stone_move)
        actions.append(move)
        total_steps += 1

    actions = ''.join(actions)
    print("UCS")  # Algorithm name
    print(f"Steps: {total_steps}, Weight: {total_weight}, Nodes: {NODES}, "
          f"Time (ms): {elapsed_time:.2f}, Memory (MB): {memory_usage:.2f}")
    print(actions)
    visualize(path)
    
    
# rrrrrruRRRRRRRurDDDDDldRR
# urrrrrrRRRRRRRRRRurDDDDDrdL