from queue import LifoQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node


def dfs(maze, ares_start, stones, switches):
    nodes = 0
    frontier = LifoQueue()
    expanded = set()  # Tập hợp để theo dõi các trạng thái đã mở rộng
    frontier_set = set()  # Kiểm tra nhanh một trạng thái đã có trong frontier

    initial_state = Node(maze, ares_start, stones, switches)
    frontier.put(initial_state)
    frontier_set.add(initial_state)
    nodes += 1

    while not frontier.empty():
        current_state = frontier.get()  # Lấy trạng thái ở đỉnh stack
        frontier_set.remove(current_state)

        if current_state in expanded:  # Kiểm tra trạng thái đã mở rộng chưa
            continue

        # Đánh dấu trạng thái hiện tại là đã mở rộng
        expanded.add(current_state)
        nodes += 1

        if current_state.is_goal():  # Kiểm tra xem có phải trạng thái đích không
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], nodes  # Trả về đường đi từ đầu đến đích

        # Lấy các trạng thái láng giềng
        neighbors = current_state.get_neighbors()

        for neighbor in neighbors:
            if neighbor not in expanded and neighbor not in frontier_set:
                if neighbor.is_goal():  # Kiểm tra trước khi thêm vào frontier
                    path = []
                    while neighbor:
                        path.append(neighbor)
                        neighbor = neighbor.prev_state
                    return path[::-1], nodes
                frontier.put(neighbor)
                frontier_set.add(neighbor)

    return None, nodes
