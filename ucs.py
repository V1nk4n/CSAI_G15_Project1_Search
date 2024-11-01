from queue import PriorityQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node

NODES = 0


def ucs(maze, ares_start, stones, switches):
    global NODES
    frontier = PriorityQueue()  # Priority queue based on cost
    expanded = set()  # Explored states
    frontier_set = set()  # For quick check if a state is in frontier

    initial_state = Node(maze, ares_start, stones, switches)
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
            return path[::-1], NODES

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
