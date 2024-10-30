

lst = [1, 2, 3, 4]
for x in lst:
    if x % 2 == 0:
        lst.remove(x)

print(lst)


    # def heuristic(self):
    #     min_h = float('inf')

    #     for stone in self.stones:
    #         ares_to_stone = manhattan_distance(self.ares, stone.position)

    #         stone_to_switch = min(manhattan_distance(
    #             stone.position, switch) for switch in self.switches)

    #         h = ares_to_stone + stone_to_switch*stone.weight

    #         min_h = min(min_h, h)

    #     return min_h

    # def heuristic(self):
    #     h = 0
    #     empty_switch = self.switches.copy()
    #     stones_by_weight = sorted(self.stones, key = lambda stone: stone.weight, reverse=True)

    #     for stone in stones_by_weight:
    #         for switch in empty_switch:
    #             if stone.position == switch:
    #                 break

    #         ares_to_stone = manhattan_distance(self.ares, stone.position)

    #         stone_to_switches, destination_switch = [manhattan_distance(stone.position, switch), switch for switch in empty_switch
    #             if self.maze[switch[0]][switch[1]] != STONE_ON_SWITCH]

    #         if stone_to_switches:
    #             stone_to_switch = min(stone_to_switches)
    #         else:
    #             stone_to_switch = 0
    #         empty_switch.remove(destination_switch)
    #         h += ares_to_stone + stone_to_switch*stone.weight
    #     return h
