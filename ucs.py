from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone
from node import Node
from queue import PriorityQueue

NODES = 0

def ucs(maze, ares_start, stones, switches):
    global NODES
    
    # Initialize priority queue for UCS, which sorts nodes by cost
    frontier = PriorityQueue()  # Priority queue based on cost
    
    # Set to store expanded (explored) states
    expanded = set()  # Explored states
    
    # Dictionary to store the lowest cost to reach each state
    cost_so_far = {}  # Cost to reach each state

    # Create the initial state node and add it to the frontier
    initial_state = Node(maze, ares_start, stones, switches)
    frontier.put((initial_state.cost, initial_state))
    cost_so_far[initial_state] = initial_state.cost
    NODES += 1

    # UCS main loop, runs until the frontier is empty
    while not frontier.empty():
        # Get the node with the lowest cost from the priority queue
        _, current_state = frontier.get()
        
        # If the current state is the goal, return the path
        if current_state.is_goal():
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], NODES
        
        # Add the current state to the expanded set
        expanded.add(current_state)
        
        # Get neighbors of the current state
        for neighbor in current_state.get_neighbors():
            new_cost = current_state.cost + 1  # Default cost for moving Ares
            for stone in neighbor.stones:
                if stone.position != current_state.stones[neighbor.stones.index(stone)].position:
                    new_cost += stone.weight  # Add stone weight if stone is moved
                    break
            
            # If the neighbor state has not been expanded or found a cheaper path
            if neighbor not in expanded:
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    neighbor.cost = new_cost
                    frontier.put((new_cost, neighbor))
                    NODES += 1
            elif new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # Remove the old neighbor from the frontier
                # Note: PriorityQueue does not support direct removal, so we need to re-add the neighbor with the updated cost
                frontier.put((new_cost, neighbor))
                neighbor.cost = new_cost

    # If no solution is found, return an empty path and the number of nodes expanded
    return [], NODES