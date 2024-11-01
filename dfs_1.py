from queue import LifoQueue  
import time
import psutil
import tracemalloc

# Các ký hiệu bản đồ
WALL = '#'
FREE = ' '
STONE = '$'
ARES = '@'
SWITCH = '.'
STONE_ON_SWITCH = '*'
ARES_ON_SWITCH = '+'

NODES = 0

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
        self.g = g
        self.prev_state = prev_state

    def __eq__(self, other):
        return (self.ares == other.ares and
                self.stones == other.stones and
                self.switches == other.switches)

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
                    new_maze[x][y] = SWITCH if (x, y) in self.switches else FREE
                    new_maze[new_x][new_y] = ARES_ON_SWITCH if new_maze[new_x][new_y] == SWITCH else ARES

                    return State(new_maze, new_ares, new_stones, self.switches, self.g + 1, self)

        if new_maze[new_x][new_y] == STONE or new_maze[new_x][new_y] == STONE_ON_SWITCH:
            return None

        new_maze[x][y] = SWITCH if (x, y) in self.switches else FREE
        new_maze[new_x][new_y] = ARES_ON_SWITCH if new_maze[new_x][new_y] == SWITCH else ARES
        return State(new_maze, new_ares, new_stones, self.switches, self.g + 1, self)

    def get_neighbors(self):
        neighbors = []
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in moves:
            new_state = self.get_state(move)
            if new_state is not None:
                neighbors.append(new_state)

        return neighbors

def dfs_limited(maze, ares_start, stones, switches, max_depth):
    global NODES
    frontier = LifoQueue()  
    expanded = set()  # Tập hợp để theo dõi các trạng thái đã mở rộng

    initial_state = State(maze, ares_start, stones, switches)
    frontier.put((initial_state, 0))  # Thêm chiều sâu của trạng thái ban đầu
    NODES += 1

    while not frontier.empty():
        current_state, depth = frontier.get()  # Lấy trạng thái và độ sâu hiện tại

        if current_state in expanded:
            continue

        expanded.add(current_state)
        
        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1]  # Trả về đường đi từ đầu đến đích

        if depth < max_depth:  # Chỉ mở rộng nếu chưa vượt quá max_depth
            neighbors = current_state.get_neighbors()
            for neighbor in neighbors:
                if neighbor not in expanded:
                    frontier.put((neighbor, depth + 1))
                    NODES += 1

    return None  # Nếu không tìm thấy đường đi trong max_depth hiện tại

def iterative_deepening_dfs(maze, ares_start, stones, switches):
    max_depth = 2
    while True:
        result = dfs_limited(maze, ares_start, stones, switches, max_depth)
        if result is not None:
            return result
        max_depth *= 2 # Tăng giới hạn độ sâu và thử lại với độ sâu lớn hơn

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

def get_move(prev_ares, curr_ares, stone_move):
    dx, dy = curr_ares[0] - prev_ares[0], curr_ares[1] - prev_ares[1]
    action = ''

    if dx == 0 and dy == -1:
        action = 'l' if not stone_move else 'L'
    elif dx == 0 and dy == 1:
        action = 'r' if not stone_move else 'R'
    elif dx == -1:
        action = 'u' if not stone_move else 'U'
    elif dx == 1:
        action = 'd' if not stone_move else 'D'

    return action

if __name__ == '__main__':
    maze_txt = input("Nhap: ")
    maze, ares_start, stones, switches = load_map(maze_txt)
    tracemalloc.start()
    start_time = time.time()
    path = iterative_deepening_dfs(maze, ares_start, stones, switches)
    end_time = time.time()
    current_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed_time = (end_time - start_time)*1000
    memory_usage = current_memory/(1024*1024)

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
    print("IDDFS")  # Tên thuật toán
    print(f"Steps: {total_steps}, Weight: {total_weight}, Nodes: {NODES}, "
          f"Memory: {memory_usage:.2f} MB, Time: {elapsed_time:.2f} ms, Actions: {actions}")
    visualize(path)