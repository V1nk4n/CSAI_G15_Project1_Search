import os
import time
import tracemalloc
from BFS import bfs, NODES
from DFS import dfs, NODES
from ucs import ucs, NODES
from astar import astar, NODES
from maze import Stone, WALL, FREE, STONE, ARES, SWITCH, ARES_ON_SWITCH, STONE_ON_SWITCH


def load_map(path):
    with open(path, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))
        maze = [list(line.strip()) for line in file.readlines()]

    stones, switches = [], []
    i_stone = 0

    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == '@' or col == '+':
                ares_start = (i, j)
            elif col == '$' or col == '*':
                stones.append(Stone((i, j), weights[i_stone]))
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


def result(maze_path, algorithm):
    maze, ares_start, stones, switches = load_map(maze_path)

    tracemalloc.start()
    start_time = time.time()

    path, NODES = algorithm(maze, ares_start, stones, switches)

    end_time = time.time()
    memory_usage = tracemalloc.get_traced_memory()[0] / (1024 * 1024)
    tracemalloc.stop()
    elapsed_time = (end_time - start_time)*1000

    step, weight = 0, 0
    steps, weights, actions = [], [], []

    for current in path[1:]:
        current_state = current
        prev_state = current.prev_state
        stone_move = 0

        for (current_stone, prev_stone) in zip(current_state.stones, prev_state.stones):
            if current_stone != prev_stone:
                weight += current_stone.weight
                weights.append(weight)
                stone_move = 1
                break

        move = get_move(prev_state.ares, current_state.ares, stone_move)
        actions.append(move)
        step += 1
        steps.append(step)

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

    # output_path = maze_path.replace("input", "output")
    # output_dir = os.path.dirname(output_path)
    # os.makedirs(output_dir, exist_ok=True)
    # with open(output_path, "w") as file:
    #     file.write(result)

    return result_str, steps, weights, actions


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
    maze_txt = r'D:\Hoc_Tap\Senior\CSAI\Lab01_Search\CSAI_G15_Project1_Search\input\input-debai.txt'
    algorithm = ucs
    result_str, steps, weights, actions = result(maze_txt, algorithm)
    print(result_str)
