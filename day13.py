import readfile
import functools
import sys
from collections import deque


# print(sys.getrecursionlimit())
# sys.setrecursionlimit(10**6)
# print(sys.getrecursionlimit())
# print()

test_data = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

A = 3
B = 1

data = readfile.read_day_file(13)



# @functools.lru_cache(maxsize=None)
def find_min_cost(cx, cy, ax, ay, bx, by, px, py, ac=0, bc=0, cost=0, max_press=100):
    stack = [(cx, cy, ax, ay, bx, by, px, py, ac, bc, cost)]
    cache = {}
    while stack:
        cx, cy, ax, ay, bx, by, px, py, ac, bc, cost = stack.pop()
        if ac > max_press or bc > max_press:
            continue
        if cx > px or cy > py:
            continue
        if (cx, cy) == (px, py):
            return True, cost
        key = (cx, cy, ax, ay, bx, by, px, py, ac, bc)
        if key in cache:
            continue
        cache[key] = cost
        stack.append((cx + ax, cy + ay, ax, ay, bx, by, px, py, ac + 1, bc, cost + A))
        stack.append((cx + bx, cy + by, ax, ay, bx, by, px, py, ac, bc + 1, cost + B))
    return False, int(1e9)

def optimized_search(cx, cy, ax, ay, bx, by, px, py, max_press=100):
    stack = deque([(cx, cy, 0, 0, 0)])
    cache = set()
    
    while stack:
        cx, cy, ac, bc, cost = stack.pop()
        
        if ac > max_press or bc > max_press:
            continue
        
        if cx > px or cy > py:
            continue
        
        if (cx, cy) == (px, py):
            return True, cost
        
        key = (cx, cy, ac, bc, cost)
        if key in cache:
            continue
        
        cache.add(key)
        
        stack.append((cx + ax, cy + ay, ac + 1, bc, cost + A))
        stack.append((cx + bx, cy + by, ac, bc + 1, cost + B))
    
    return False, int(1e9)

def part_one():
    p1_data = data.strip().split("\n\n")
    _sum = 0
    for m in p1_data:
        l1, l2, l3 = m.split("\n")
        l1 = l1.split(": ")[-1].split(", ")
        ax, ay = int(l1[0][2:]), int(l1[1][2:])
        l2 = l2.split(": ")[-1].split(", ")
        bx, by = int(l2[0][2:]), int(l2[1][2:])
        l3 = l3.split(": ")[-1].split(", ")
        px, py = int(l3[0][2:]), int(l3[1][2:])
        min_cost = find_min_cost(0, 0, ax, ay, bx, by, px, py)
        if min_cost[0]:
            # print(min_cost[1])
            _sum += min_cost[1]
    print(_sum)
        # break

def find_intersection(a, b, c, a1, b1, c1):
    # Calculate the determinant
    determinant = a * b1 - a1 * b
    if determinant == 0:
        return None, None

    # Calculate the intersection point
    x = (c * b1 - c1 * b) / determinant
    y = (a * c1 - a1 * c) / determinant

    if int(x) != x or int(y) != y:
        return None, None
    
    return x, y

def part_two():
    p2_data = data.strip().split("\n\n")
    _sum = 0
    extra_pos = 10_000_000_000_000
    for m in p2_data:
        l1, l2, l3 = m.split("\n")
        l1 = l1.split(": ")[-1].split(", ")
        ax, ay = int(l1[0][2:]), int(l1[1][2:])
        l2 = l2.split(": ")[-1].split(", ")
        bx, by = int(l2[0][2:]), int(l2[1][2:])
        l3 = l3.split(": ")[-1].split(", ")
        px, py = int(l3[0][2:]), int(l3[1][2:])
        # min_cost = find_min_cost(0, 0, ax, ay, bx, by, px + extra_pos, py + extra_pos, max_press=int(1e4))
        # min_cost = optimized_search(0, 0, ax, ay, bx, by, px + extra_pos, py + extra_pos, max_press=int(10000))
        ac, bc = find_intersection(ax, bx, px + extra_pos, ay, by, py + extra_pos)
        if ac is None:
            continue
        _sum += ac * A + bc * B

    print(_sum)

part_two()