import readfile
import numpy as np

test_data = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

data = readfile.read_day_file(10).strip()

def part_one():
    p1data = data
    arr = np.array(
        [list(map(int, list(x))) for x in p1data.splitlines()]
    )
    # get all coordinates of 0's
    zeros = np.argwhere(arr == 0)
    nines = np.argwhere(arr == 9)
    def walk_trail(arr, x, y, visited=None):
        if visited is None:
            visited = set()
        if (x, y) in visited:
            return 0
        visited.add((x, y))
        if not (0 <= x < arr.shape[0] and 0 <= y < arr.shape[1]):
            return 0
        if arr[x, y] == 9:
            return 1
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        directions = [(x+dx, y+dy) for dx, dy in directions if 0 <= x+dx < arr.shape[0] and 0 <= y+dy < arr.shape[1] and arr[x+dx, y+dy] - arr[x ,y] == 1]
        return sum(walk_trail(arr, x, y, visited) for x, y in directions)
    
    _sum = 0
    for x, y in zeros:
        score = walk_trail(arr, x, y)
        # print(score)
        _sum += score
    print(_sum)

def part_two():
    p1data = data
    arr = np.array(
        [list(map(int, list(x))) for x in p1data.splitlines()]
    )
    # get all coordinates of 0's
    zeros = np.argwhere(arr == 0)
    nines = np.argwhere(arr == 9)
    def walk_trail(arr, x, y, visited=None):
        if visited is None:
            visited = set()
        # if (x, y) in visited:
        #     return 0
        visited.add((x, y))
        if not (0 <= x < arr.shape[0] and 0 <= y < arr.shape[1]):
            return 0
        if arr[x, y] == 9:
            return 1
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        directions = [(x+dx, y+dy) for dx, dy in directions if 0 <= x+dx < arr.shape[0] and 0 <= y+dy < arr.shape[1] and arr[x+dx, y+dy] - arr[x ,y] == 1]
        return sum(walk_trail(arr, x, y, visited) for x, y in directions)
    
    _sum = 0
    for x, y in zeros:
        score = walk_trail(arr, x, y)
        # print(score)
        _sum += score
    print(_sum)

part_two()