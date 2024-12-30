import readfile
import numpy as np
import time
import copy

data = readfile.read_day_file(15)

test_data = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

# test_data = """\
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^
# """

def part_one():
    p1data = data.strip().split("\n\n")
    grid = np.array([list(x) for x in p1data[0].split("\n")])
    n, m = grid.shape
    instructions = ''.join(p1data[1].split("\n"))
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    fish = np.where(grid == '@')
    fish = (fish[0][0], fish[1][0])

    def check_valid(x, y):
        return 0 <= x < n and 0 <= y < m
    
    for i in instructions:
        dx, dy = directions[i]
        fx, fy = fish
        obs = grid[fx + dx][fy + dy]
        if obs == '#':
            continue
        elif obs == '.':
            grid[fx][fy] = '.'
            fish = (fx + dx, fy + dy)
            grid[fx + dx][fy + dy] = '@'
        elif obs == 'O':
            # push box towards direction
            bx, by = fx + dx, fy + dy
            while check_valid(bx,by) and grid[bx][by] == 'O':
                bx, by = bx + dx, by + dy
            if not check_valid(bx, by) or grid[bx][by] == '#':
                continue
            opx, opy = dx * -1, dy * -1
            while (bx, by) != (fx, fy):
                grid[bx][by] = 'O'
                bx, by = bx + opx, by + opy
            grid[fx][fy] = '.'
            fish = (fx + dx, fy + dy)
            grid[fx + dx][fy + dy] = '@'
        # print(grid)
    box_locs = np.where(grid == 'O')
    _sum = 0
    for (i, j) in zip(*box_locs):
        _sum += 100 * i + j
    print(_sum)

def part_two():
    p1data = data.strip().split("\n\n")
    grid = []
    for line in p1data[0].split("\n"):
        row = []
        for c in line:
            if c == '#':
                row.append("#")
                row.append("#")
            elif c == 'O':
                row.append("[")
                row.append("]")
            elif c == '@':
                row.append("@")
                row.append(".")
            elif c == ".": 
                row.append(".")
                row.append(".")
        grid.append(row)
    grid = np.array(grid)
    n, m = grid.shape
    instructions = ''.join(p1data[1].split("\n"))
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    fish = np.where(grid == '@')
    fish = (fish[0][0], fish[1][0])

    def check_valid(x, y):
        return 0 <= x < n and 0 <= y < m
    
    def get_connected_boxes(bx, by, dx, dy, boxes=None):
        if boxes is None:
            boxes = set()
        if not check_valid(bx, by):
            return boxes
        if grid[bx][by] == '#':
            return boxes
        if grid[bx][by] == '.':
            return boxes
        bx1, by1 = bx, by
        if grid[bx][by] == '[':
            by1 += 1
        elif grid[bx][by] == ']':
            by -= 1
        up_down = dx != 0
        boxes.add((bx, by, bx1, by1))
        if up_down:
            if grid[bx + dx][by + dy] in {'[', ']'} and grid[bx + dx][by + dy] in {'[', ']'}:
                get_connected_boxes(bx + dx, by + dy, dx, dy, boxes)
                get_connected_boxes(bx1 + dx, by1 + dy, dx, dy, boxes)
            elif grid[bx + dx][by + dy] in {'[', ']'}:
                get_connected_boxes(bx + dx, by + dy, dx, dy, boxes)
            elif grid[bx1 + dx][by1 + dy] in {'[', ']'}:
                get_connected_boxes(bx1 + dx, by1 + dy, dx, dy, boxes)
        else:
            left = dy == -1
            if left:
                get_connected_boxes(bx + dx, by + dy, dx, dy, boxes)
            else:
                get_connected_boxes(bx1 + dx, by1 + dy, dx, dy, boxes)
        return boxes
    
    for k, i in enumerate(instructions):
        if k == 1306:
            k =k
        dx, dy = directions[i]
        fx, fy = fish
        obs = grid[fx + dx][fy + dy]
        if obs == '#':
            obs = obs
        elif obs == '.':
            grid[fx][fy] = '.'
            fish = (fx + dx, fy + dy)
            grid[fx + dx][fy + dy] = '@'
        elif obs in {'[', ']'}:
            bx0, by0 = fx + dx, fy + dy
            boxes = get_connected_boxes(bx0, by0, dx, dy)
            should_move = True
            # test_values = []
            # for bx, by, bx1, by1 in boxes:
            #     test_values.append(grid[bx][by] + grid[bx1][by1])
            for bx, by, bx1, by1 in boxes:
                if not check_valid(bx + dx, by + dy) or grid[bx + dx][by + dy] == '#' or \
                not check_valid(bx1 + dx, by1 + dy) or grid[bx1 + dx][by1 + dy] == '#':
                    should_move = False
                    break
            if should_move:
                for bx, by, bx1, by1 in boxes:
                    grid[bx][by] = '.'
                    grid[bx1][by1] = '.'

                for bx, by, bx1, by1 in boxes:
                    grid[bx + dx][by + dy] = '['
                    grid[bx1 + dx][by1 + dy] = ']'
                grid[fx][fy] = '.'
                fish = (fx + dx, fy + dy)
                grid[fx + dx][fy + dy] = '@'
        print(i, k)
        print('\n'.join(''.join(x) for x in grid))
        print()
    box_locs = np.where(grid == '[')

    _sum = 0
    for (i, j) in zip(*box_locs):
        _sum += 100 * i + j
    print(_sum)

# part_one()
part_two()