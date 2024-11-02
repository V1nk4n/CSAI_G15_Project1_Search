from queue import LifoQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node


def dfs_limited(maze, ares_start, stones, switches, max_depth):
    nodes = 0
    frontier = LifoQueue()
    expanded = set()  # Tập hợp để theo dõi các trạng thái đã mở rộng

    initial_state = Node(maze, ares_start, stones, switches)
    frontier.put((initial_state, 0))  # Thêm chiều sâu của trạng thái ban đầu
    nodes += 1

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
            return path[::-1], nodes  # Trả về đường đi từ đầu đến đích

        if depth < max_depth:  # Chỉ mở rộng nếu chưa vượt quá max_depth
            neighbors = current_state.get_neighbors()
            for neighbor in neighbors:
                if neighbor not in expanded:
                    frontier.put((neighbor, depth + 1))
                    nodes += 1

    return None, nodes  # Nếu không tìm thấy đường đi trong max_depth hiện tại


def dfs(maze, ares_start, stones, switches):
    max_depth = 2
    while True:
        result, nodes = dfs_limited(maze, ares_start, stones, switches, max_depth)
        if result is not None:
            return result, nodes
        max_depth *= 2  # Tăng giới hạn độ sâu và thử lại với độ sâu lớn hơn
