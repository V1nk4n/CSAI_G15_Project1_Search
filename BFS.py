from queue import Queue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node

NODES = 0


def bfs(maze, ares_start, stones, switches):
    global NODES

    initial_state = Node(maze, ares_start, stones, switches)

    if initial_state.is_goal():
        print('Ares đã thành công!')
        return None

    frontier = Queue()
    frontier.put(initial_state)
    NODES += 1
    # Lưu các trạng thái để dễ dàng kiểm tra một trạng thái đã có trong frontier hay chưa
    frontier_set = set()
    frontier_set.add(initial_state)
    expanded = set()

    while frontier.empty() == False:
        current_state = frontier.get()
        frontier_set.remove(current_state)
        expanded.add(current_state)
        NODES += 1
        # Lấy các trạng thái có thể có từ trạng thái hiện tại
        neighbors = current_state.get_neighbors()

        for neighbor in neighbors:
            # Bỏ qua trạng thái đã được mở rộng
            if ((neighbor not in expanded) and (neighbor not in frontier_set)):
                if neighbor.is_goal():
                    goal_state = neighbor
                    path = []
                    # Lưu trạng thái từ đích -> ban đầu
                    while goal_state:
                        path.append(goal_state)
                        goal_state = goal_state.prev_state
                    # Trả về đường đi từ trạng thái đầu -> đích
                    return path[::-1], NODES

                frontier.put(neighbor)
                frontier_set.add(neighbor)

    return None
