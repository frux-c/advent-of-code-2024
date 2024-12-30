import readfile
import numpy as np
import time

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

test_data = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

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
    
    def move_box_rec(bx, by, dx, dy, moves=[]):
        if not check_valid(bx, by):
            return False
        
        bx1, by1 = bx, by
        if grid[bx][by] == ']':
            by -= 1
        else:
            by1 += 1
        up_down = (dx, dy) == (-1, 0) or (dx, dy) == (1, 0)
        left = (dx, dy) == (0, -1)
        right = (dx, dy) == (0, 1)
        
        # check if box can move
        if up_down and not check_valid(bx + dx, by + dy) or grid[bx + dx][by + dy] == '#':
            return False
        if left and not check_valid(bx + dx, by + dy) or grid[bx + dx][by + dy] == '#':
            return False
        if right and not check_valid(bx1 + dx, by1 + dy) or grid[bx1 + dx][by1 + dy] == '#':
            return False
        if up_down:
            a = True
            # check if there is a box aligned in the way
            if grid[bx + dx][by + dy] == '[' and grid[bx1 + dx][by1 + dy] == ']':
                a = move_box_rec(bx + dx, by + dy, dx, dy, moves)
            # check if there are boxes in the way
            elif grid[bx + dx][by + dy] in {'[', ']'} and grid[bx1 + dx][by1 + dy] in {'[', ']'}:
                a = move_box_rec(bx + dx, by + dy, dx, dy, moves) and move_box_rec(bx1 + dx, by1 + dy, dx, dy, moves)
            # there is one box in the way
            elif grid[bx + dx][by + dy] in {'[', ']'}:
                a =  move_box_rec(bx + dx, by + dy, dx, dy, moves)
            # there is one box in the way
            elif grid[bx1 + dx][by1 + dy] in {'[', ']'}:
                a = move_box_rec(bx1 + dx, by1 + dy, dx, dy, moves)
            # move the box
            moves.append((bx, by, '.'))
            moves.append((bx1, by1, '.'))
            moves.append((bx + dx, by + dy, '['))
            moves.append((bx1 + dx, by1 + dy, ']'))
            return a
        # move box left or right
        a = True
        if left:
            if check_valid(bx + dx * 2, by + dy * 2) and \
                grid[bx + dx][by + dy] in {'[', ']'}:
                a = move_box_rec(bx + dx * 2, by + dy * 2, dx, dy, moves)
        else:
            if check_valid(bx1 + dx * 2, by1 + dy * 2) and \
                grid[bx1 + dx][by1 + dy] in {'[', ']'}:
                a = move_box_rec(bx1 + dx * 2, by1 + dy * 2, dx, dy, moves)
        moves.append((bx + dx, by + dy, grid[bx][by]))
        moves.append((bx1 + dx, by1 + dy, grid[bx1][by1]))
        return a


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
            moves = []
            shoud_move = move_box_rec(bx0, by0, dx, dy, moves)
            if shoud_move:
                for bx, by, c in moves:                        
                    grid[bx][by] = c
                    if k >= 1306:
                        # print('\n'.join(''.join(x) for x in grid))
                        1 == 1
                if k >= 1306:
                    1 == 1
                grid[fx][fy] = '.'
                fish = (fx + dx, fy + dy)
                grid[fx + dx][fy + dy] = '@'
        # time.sleep(1/15)
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