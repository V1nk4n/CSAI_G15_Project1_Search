import os
import time
import tracemalloc
from bfs import bfs
from dfs import dfs
from ucs import ucs
from astar import astar
from maze import Stone, WALL, FREE, STONE, ARES, SWITCH, ARES_ON_SWITCH, STONE_ON_SWITCH


def load_map(path):
    with open(path, 'r') as file:
        first_line = file.readline().strip()
        weights = list(map(int, first_line.split()))
        maze = [line for line in file.readlines()]

    i_stone = 0
    stones = []
    switches = []

    maze = [x.replace('\n', '') for x in maze]
    maze = [','.join(maze[i]) for i in range(len(maze))]
    maze = [x.split(',') for x in maze]
    maxColsNum = max([len(x) for x in maze])
    for irow in range(len(maze)):
        for icol in range(len(maze[irow])):
            if maze[irow][icol] == '@' or maze[irow][icol] == '+':
                ares_start = (irow, icol)
            elif maze[irow][icol] == '$' or maze[irow][icol] == '*':
                stone_position = (irow, icol)
                stone_weight = weights[i_stone]
                stone = Stone(stone_position, stone_weight)
                stones.append(stone)
                i_stone += 1
            elif maze[irow][icol] == '.':
                switches.append((irow, icol))
        colsNum = len(maze[irow])
        if colsNum < maxColsNum:
            maze[irow].extend(['#' for _ in range(maxColsNum-colsNum)])

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


def result(maze_path, algorithm):
    maze, ares_start, stones, switches = load_map(maze_path)

    tracemalloc.start()
    start_time = time.time()

    path, NODES = algorithm(maze, ares_start, stones, switches)

    end_time = time.time()
    memory_usage = tracemalloc.get_traced_memory()[0] / (1024 * 1024)
    tracemalloc.stop()
    elapsed_time = (end_time - start_time)*1000

    step, weight, cost = 0, 0, 0
    steps, weights, actions, costs = [], [], [], []

    for current in path[1:]:
        prev_state = current.prev_state
        stone_move = 0

        for (current_stone, prev_stone) in zip(current.stones, prev_state.stones):
            if current_stone != prev_stone:
                weight += current_stone.weight

                stone_move = 1
                break

        step += 1
        move = get_move(prev_state.ares, current.ares, stone_move)
        cost = current.cost

        steps.append(step)
        weights.append(weight)
        actions.append(move)
        costs.append(cost)

    actions_str = ''.join(actions)

    if algorithm == bfs:
        algorithm_name = "BFS"

    if algorithm == dfs:
        algorithm_name = "DFS"

    if algorithm == ucs:
        algorithm_name = "UCS"

    if algorithm == astar:
        algorithm_name = "A*"

    result_str = f'{algorithm_name}\nSteps: {step}, Weight: {weight}, Nodes: {NODES}, Time (ms): {elapsed_time:.2f}, Memory (MB): {memory_usage:.2f}\n{actions_str}'

    return result_str, weights, costs


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


def solve(maze_path):
    results_output = []
    results_gui = []

    bfs_str, bfs_weights, bfs_costs = result(maze_path, bfs)
    results_output.append(bfs_str)
    results_gui.append(bfs_str)
    results_gui.append(bfs_weights)
    results_gui.append(bfs_costs)

    dfs_str, dfs_weights, dfs_costs = result(maze_path, dfs)
    results_output.append(dfs_str)
    results_gui.append(dfs_str)
    results_gui.append(dfs_weights)
    results_gui.append(dfs_costs)

    ucs_str, ucs_weights, ucs_costs = result(maze_path, ucs)
    results_output.append(ucs_str)
    results_gui.append(ucs_str)
    results_gui.append(ucs_weights)
    results_gui.append(ucs_costs)

    astar_str, astar_weights, astar_costs = result(
        maze_path, astar)
    results_output.append(astar_str)
    results_gui.append(astar_str)
    results_gui.append(astar_weights)
    results_gui.append(astar_costs)

    results_output = '\n'.join(results_output)
    print(results_output)

    output_path = maze_path.replace("input", "output")
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as file:
        file.write(results_output)

    output_gui_path = maze_path.replace("input", "output-gui")
    output_gui_dir = os.path.dirname(output_gui_path)
    os.makedirs(output_gui_dir, exist_ok=True)
    with open(output_gui_path, "w") as file:
        file.write(results_gui)


if __name__ == '__main__':
    # for i in range(10):
    #     print(f'Maze {i+1}')
    #     maze_path = f'input\\input-0{i+1}.txt'
    #     if i >= 10:
    #         maze_path = f'input\\input-{i+1}.txt'
    #     print(maze_path)

    maze_path = f'input\\input-01.txt'
    bfs_str, bfs_steps, bfs_weights, bfs_actions = result(maze_path, astar)
    print(bfs_str)
    print(bfs_weights)
