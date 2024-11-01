from queue import PriorityQueue
from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node

NODES = 0

def ucs(maze, ares_start, stones, switches):
    global NODES
    
    # Initialize priority queue for UCS, which sorts nodes by cost
    frontier = PriorityQueue()  # Priority queue based on cost
    
    # Set to store expanded (explored) states
    expanded = set()  # Explored states
    
    # Set to quickly check if a state is in the frontier
    frontier_set = set()  # For quick check if a state is in frontier

    # Create the initial state node and add it to the frontier
    initial_state = Node(maze, ares_start, stones, switches)
    frontier.put((initial_state.cost, initial_state))
    frontier_set.add(initial_state)
    NODES += 1

    # UCS main loop, runs until the frontier is empty
    while not frontier.empty():
        # Get the node with the lowest cost from the priority queue
        _, current_state = frontier.get()
        frontier_set.remove(current_state)

        # Check if the current state is the goal state
        if current_state.is_goal():
            # If goal is reached, reconstruct the path from start to goal
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], NODES

        # Add the current state to the set of expanded states
        expanded.add(current_state)

        # Get all the neighbor states (valid moves) from the current state
        neighbors = current_state.get_neighbors()
        for neighbor in neighbors:
            # Skip neighbor if it has already been expanded
            if neighbor in expanded:
                continue

            # If the neighbor is not in the frontier, add it
            if neighbor not in frontier_set:
                frontier.put((neighbor.cost, neighbor))
                frontier_set.add(neighbor)
                NODES += 1

    # Return None if no solution is found
    return None
