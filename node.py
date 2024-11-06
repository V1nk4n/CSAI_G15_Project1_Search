from maze import WALL, FREE, STONE, ARES, SWITCH, STONE_ON_SWITCH, ARES_ON_SWITCH, Stone


class Node:
    def __init__(self, maze, ares, stones, switches, g=0, prev_state=None):
        self.maze = [row[:] for row in maze]
        self.ares = ares
        self.stones = stones
        self.switches = switches
        self.cost = g
        self.prev_state = prev_state

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return (self.ares == other.ares and
                self.stones == other.stones and
                self.switches == other.switches)

    def __lt__(self, other):
        return self.cost < other.cost

    def __hash__(self):
        return hash((self.ares, tuple(self.stones), tuple(self.switches)))

    # Kiểm tra trạng thái đích
    def is_goal(self):
        return all(stone.position in self.switches for stone in self.stones)

    def get_state(self, move):
        width, height = len(self.maze), len(self.maze[0])

        # Tìm vị trí mới của ares
        x_ares, y_ares = self.ares
        new_x_ares, new_y_ares = x_ares + move[0], y_ares + move[1]

        # Kiểm tra vị trí mới có vượt ra khỏi mê cung không?
        if not (0 <= new_x_ares < width and 0 <= new_y_ares < height):
            return None

        # Kiểm tra vị trí mới của ares có phải là tường không?
        if self.maze[new_x_ares][new_y_ares] == WALL:
            return None

        # Khởi tạo mê cung, ares và các viên đá của trạng thái mới
        new_maze = [row[:] for row in self.maze]
        new_ares = (new_x_ares, new_y_ares)
        new_stones = list(self.stones)

        for i_stone, stone in enumerate(self.stones):
            # Kiểm tra nếu vị trí mới của ares là viên đá thì tiến hành đẩy viên đá
            if (new_x_ares, new_y_ares) == stone.position:
                # Tính toán vị trí mới của đá
                new_x_stone, new_y_stone = new_x_ares + \
                    move[0], new_y_ares + move[1]

                # Kiểm tra vị trí mới của viên đá phải nằm trong mê cung và phải nằm ở những ô trống hoặc công tắc
                if (0 <= new_x_stone < width and 0 <= new_y_stone < height and
                        new_maze[new_x_stone][new_y_stone] in (FREE, SWITCH)):

                    # Cập nhật lại viên đá đã được đẩy
                    new_stone = Stone((new_x_stone, new_y_stone), stone.weight)
                    new_stones[i_stone] = new_stone

                    # Cập nhật mê cung
                    new_maze[new_x_stone][new_y_stone] = STONE_ON_SWITCH if new_maze[new_x_stone][new_y_stone] == SWITCH else STONE
                    new_maze[x_ares][y_ares] = SWITCH if (
                        x_ares, y_ares) in self.switches else FREE
                    new_maze[new_x_ares][new_y_ares] = ARES_ON_SWITCH if new_maze[new_x_ares][new_y_ares] == SWITCH else ARES

                    # Cập nhật chi phí cộng thêm 1 bước đi và trọng lượng của đá
                    new_cost = self.cost + 1 + stone.weight

                    return Node(new_maze, new_ares, new_stones, self.switches, new_cost, self)

        # Kiểm tra đảm bảo vị trí mới của ares không phải là đá (trong trường hợp không thể đẩy đá)
        if new_maze[new_x_ares][new_y_ares] in (STONE, STONE_ON_SWITCH):
            return None

        # Cập nhật mê cung
        new_maze[x_ares][y_ares] = SWITCH if (
            x_ares, y_ares) in self.switches else FREE
        new_maze[new_x_ares][new_y_ares] = ARES_ON_SWITCH if new_maze[new_x_ares][new_y_ares] == SWITCH else ARES

        # Cập nhật chi phí cộng thêm một bước
        new_cost = self.cost + 1

        return Node(new_maze, new_ares, new_stones, self.switches, new_cost, self)

    # Kiểm tra đá có nằm trong góc hay không?
    def stone_in_corner(self):
        for stone in self.stones:
            if stone.position not in self.switches:
                x, y = stone.position
                if ((self.maze[x-1][y] == WALL or self.maze[x+1][y] == WALL)
                        and (self.maze[x][y-1] == WALL or self.maze[x][y+1] == WALL)):
                    return True
        return False

    # Tìm các trạng thái kề cận với 4 bước di chuyển: lên, xuống, trái, phải
    def get_neighbors(self):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        # Danh sách chứa các hàng xóm kề cận
        neighbors = []

        # Duyệt qua từng bước di chuyển
        for move in moves:
            # TÌm trạng thái tiếp theo
            next_state = self.get_state(move)
            # Nếu trạng thái tiếp theo khác None và không có viên đá nằm ở góc thì thêm vào danh sách các hàng xóm
            if next_state and not next_state.stone_in_corner():
                neighbors.append(next_state)
        return neighbors
