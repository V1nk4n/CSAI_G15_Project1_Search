from queue import LifoQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node

NODES = 0


def dfs(maze, ares_start, stones, switches):
    global NODES
    frontier = LifoQueue()
    expanded = set()  # Tập hợp để theo dõi các trạng thái đã mở rộng
    frontier_set = set()  # Kiểm tra nhanh một trạng thái đã có trong frontier

    initial_state = Node(maze, ares_start, stones, switches)
    frontier.put(initial_state)
    frontier_set.add(initial_state)

    NODES += 1

    while not frontier.empty():
        current_state = frontier.get()  # Lấy trạng thái ở đỉnh stack
        frontier_set.remove(current_state)
        if current_state in expanded:  # Kiểm tra trạng thái đã mở rộng chưa
            continue

        # Đánh dấu trạng thái hiện tại là đã mở rộng
        expanded.add(current_state)
        NODES += 1

        if current_state.is_goal():  # Kiểm tra xem có phải trạng thái đích không
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], NODES  # Trả về đường đi từ đầu đến đích

        # Lấy các trạng thái láng giềng
        neighbors = current_state.get_neighbors()

        for neighbor in neighbors:
            if neighbor not in frontier_set:  # Thêm trạng thái vào frontier nếu chưa mở rộng
                frontier.put(neighbor)
                frontier_set.add(neighbor)

    return None
