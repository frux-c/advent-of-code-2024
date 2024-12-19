import readfile
import copy
import numpy as np
from itertools import combinations 
data = readfile.read_day_file(8)

test_data = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
# test_data = """\
# .........a
# ..........
# ..........
# ..........
# .....a..a.
# ..........
# ..........
# ..........
# ..........
# ..........
# """

expected_data = """\
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
"""

expected_data2 = """\
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
"""

def part_one():
    p1data = copy.deepcopy(data).strip()
    arr = [[col for col in row] for row in p1data.split('\n')]
    arr = np.array(arr, dtype='U')
    print(arr.shape)
    # finda all unique values that are not '.'
    unique_values = np.unique(arr)
    unique_values = unique_values[unique_values != '.']
    # find all locations of unique values
    dict_locations = {value: list((x,y) for x, y in zip(*np.where(arr == value))) for value in unique_values}
    antinode_locations = set()
    for key in dict_locations:
        for p1, p2 in combinations(dict_locations[key], 2):
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2:
                dx, dy = 0, y2 - y1
            elif x1 > x2:
                dx, dy = x1 - x2, y1 - y2
            else:
                dx, dy = x2 - x1, y2 - y1
            # antinodes have to be 2x the distance of the current distance
            nx1, ny1 = \
                x1 - dx, y1 - dy
            nx2, ny2 = \
                x2 + dx, y2 + dy
            if 0 <= nx1 < arr.shape[0] and 0 <= ny1 < arr.shape[1]:
                antinode_locations.add((nx1, ny1))
            if 0 <= nx2 < arr.shape[0] and 0 <= ny2 < arr.shape[1]:
                antinode_locations.add((nx2, ny2))
            # # get the y=mx+b equation
            # if dx == 0:
            #     nx1, ny1 = x1, y1
            #     nx2, ny2 = x2, y2
            #     curr_c_distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            #     while True:
            #         c_distance = np.sqrt((nx2 - nx1) ** 2 + (ny2 - ny1) ** 2)
            #         if c_distance >= curr_c_distance * 2:
            #             break
            #         ny1 += dy
            #         ny2 -= dy
            # else:
            #     b = y1 - (dy / dx) * x1
            #     fx = lambda x: int((dy / dx) * x + b)
            #     nx1, ny1 = x1, y1
            #     nx2, ny2 = x2, y2
            #     curr_c_distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            #     while True:
            #         c_distance = np.sqrt((nx2 - nx1) ** 2 + (ny2 - ny1) ** 2)
            #         if c_distance >= curr_c_distance * 2:
            #             break
            #         nx1, ny1 = nx1 + dx, fx(nx1 + dx)
            #         nx2, ny2 = nx2 - dx, fx(nx2 - dx)
            # if 0 <= nx1 < arr.shape[0] and 0 <= ny1 < arr.shape[1]:
            #     antinode_locations.add((nx1, ny1))
            # if 0 <= nx2 < arr.shape[0] and 0 <= ny2 < arr.shape[1]:
            #     antinode_locations.add((nx2, ny2))

    print(len(antinode_locations))

def part_two():
    p2data = copy.deepcopy(data).strip()
    arr = [[col for col in row] for row in p2data.split('\n')]
    arr = np.array(arr, dtype='U')
    print(arr.shape)
    # finda all unique values that are not '.'
    unique_values = np.unique(arr)
    unique_values = unique_values[unique_values != '.']
    # find all locations of unique values
    dict_locations = {value: list((x,y) for x, y in zip(*np.where(arr == value))) for value in unique_values}
    antinode_locations = set()
    for key in dict_locations:
        for p1, p2 in combinations(dict_locations[key], 2):
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2:
                dx, dy = 0, y2 - y1
            elif x1 > x2:
                dx, dy = x1 - x2, y1 - y2
            else:
                dx, dy = x2 - x1, y2 - y1
            # antinodes have to be 2x the distance of the current distance
            antinode_locations.add((x1,y1))
            antinode_locations.add((x2,y2))
            nx1, ny1 = \
                x1 - dx, y1 - dy
            nx2, ny2 = \
                x2 + dx, y2 + dy
            while 0 <= nx1 < arr.shape[0] and 0 <= ny1 < arr.shape[1]:
                antinode_locations.add((nx1, ny1))
                nx1, ny1 = \
                nx1 - dx, ny1 - dy
            while 0 <= nx2 < arr.shape[0] and 0 <= ny2 < arr.shape[1]:
                antinode_locations.add((nx2, ny2))
                nx2, ny2 = \
                nx2 + dx, ny2 + dy
    print(len(antinode_locations))
    # for x, y in antinode_locations:
    #     if arr[x, y] == '.':
    #         arr[x, y] = '#'
    # print(arr)
    # js = '\n'.join([''.join(row) for row in arr])
    # print(js)

# part_one()
part_two()