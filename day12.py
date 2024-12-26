import readfile
import numpy as np
import copy


# test_data = """\
# RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE
# """

test_data = """\
AAAA
BBCD
BBCC
EEEC
"""

data = readfile.read_day_file(12).strip()

def traverse_letter(arr, x, y, l, visited_per_letter):
    # l = letter
    stack = [(x, y)]
    perimeters = set()
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= arr.shape[0] or y < 0 or y >= arr.shape[1]:
            perimeters.add((x, y))
            continue
        if arr[x][y] != l:
            perimeters.add((x, y))
            continue
        if (x, y) in visited_per_letter[l]:
            continue
        visited_per_letter[l].add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            stack.append((x+dx, y+dy))
    return perimeters

def count_perimeters(arr, perimeters, current_visited):
    count = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while perimeters:
        x, y = perimeters.pop()
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if nx < 0 or nx >= arr.shape[0] or ny < 0 or ny >= arr.shape[1]:
                continue
            if (nx, ny) in current_visited:
                count += 1
    return count

def traverse_letter_v2(arr, x, y, l, visited_per_letter):
    # l = letter
    stack = [(x, y)]
    perimeters = set()
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= arr.shape[0] or y < 0 or y >= arr.shape[1]:
            continue
        if arr[x][y] != l:
            perimeters.add((x, y))
            continue
        if (x, y) in visited_per_letter[l]:
            continue
        visited_per_letter[l].add((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            stack.append((x+dx, y+dy))
    return perimeters

def get_bounded_array(arr, region):
    min_x, min_y = min(region, key=lambda x: x[0])[0], min(region, key=lambda x: x[1])[1]
    max_x, max_y = max(region, key=lambda x: x[0])[0], max(region, key=lambda x: x[1])[1]
    return arr[min_x:max_x+1, min_y:max_y+1]

def get_straight_options(arr, x, y, perimeter, visited):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    options = []
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if nx < 0 or nx >= arr.shape[0] or ny < 0 or ny >= arr.shape[1]:
            continue
        if (nx, ny) in perimeter and (nx, ny) not in visited:
            options.append((nx, ny, dx, dy))
    return options

def get_adjecent_sides(arr, x, y, perimeter, visited=None):
    directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
    options = []
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if nx < 0 or nx >= arr.shape[0] or ny < 0 or ny >= arr.shape[1]:
            continue
        if (nx, ny) in perimeter and (nx, ny) not in visited:
            options.append((nx, ny, dx, dy))
    return options

def get_perimeter_wall(arr, x, y, region, vregion):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    walls = set()
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if nx < 0 or nx >= arr.shape[0] or ny < 0 or ny >= arr.shape[1]:
            continue
        if (nx, ny) in region and (nx, ny) not in vregion:
            walls.add((nx, ny))
    return walls

def is_right_angle(p1, p2, p3):
    # Calculate the squared lengths of the sides of the triangle
    a2 = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
    b2 = (p3[0] - p2[0])**2 + (p3[1] - p2[1])**2
    c2 = (p3[0] - p1[0])**2 + (p3[1] - p1[1])**2
    
    # Check if any combination of sides satisfies the Pythagorean theorem
    return a2 + b2 == c2 or a2 + c2 == b2 or b2 + c2 == a2

corners = [
        np.array([[1, 0], 
                  [0, 0]]),
        np.array([[0, 1], 
                  [0, 0]]),
        np.array([[0, 0], 
                  [1, 0]]),
        np.array([[0, 0], 
                  [0, 1]]),
        np.array([[0, 1], 
                  [1, 1]]),
        np.array([[1, 0], 
                  [1, 1]]),
        np.array([[1, 1], 
                  [0, 1]]),
        np.array([[1, 1], 
                  [1, 0]])
    ]

special_corners = [
    np.array([[1, 0],
              [0, 1]]),
    np.array([[0, 1],
              [1, 0]])
]

def is_corner(arr):
    count = 0
    for corner in corners:
        if np.array_equal(arr, corner):
            count += 1
    for corner in special_corners:
        if np.array_equal(arr, corner):
            count += 2
    return count

def count_adjecent_sides_helper(arr, x, y, dx, dy, perimeters, region, vperimeter=None):
    if not vperimeter:
        vperimeter = set()
    stack = [(x, y, dx, dy, 0, vperimeter, set(), [])]
    i = 0
    path_stack = []
    while stack:
        x, y, dx, dy, count, vperimeter, vregion, pstack = stack.pop()
        i += 1
        if len(vperimeter) == len(perimeters):
            path_stack = pstack
            break
        s = get_straight_options(arr, x, y, perimeters, vperimeter)
        d = get_adjecent_sides(arr, x, y, perimeters, vperimeter)
        w = get_perimeter_wall(arr, x, y, region, set())
        ## DEBUG ###
        # tmp = arr[x,y]
        # arr[x,y] = '*'
        # print(arr)
        # print((x, y), count, w)
        # arr[x,y] = tmp
        ## DEBUG ###
        # print(f"X: {x}, Y: {y}\nDX: {dx}, DY: {dy}\nCount: {count}\nPerimeter: {vperimeter}\nRegion: {vregion}\n")
        if not s:
            if not d:
                continue
            for nx, ny, dx2, dy2 in d:
                stack.append((nx, ny, dx2, dy2, count + len(w), vperimeter | {(nx, ny)}, vregion | w, pstack + [(nx, ny)]))
        else:
            for nx, ny, dx2, dy2 in s:
                if dx == dx2 and dy == dy2 or dx == 0 and dy == 0:
                    stack.append((nx, ny, dx2, dy2, count, vperimeter | {(nx, ny)}, vregion | w, pstack + [(nx, ny)]))
                else:
                    stack.append((nx, ny, dx2, dy2, count + len(w), vperimeter | {(nx, ny)}, vregion | w, pstack + [(nx, ny)]))
    
    # for x, y in path_stack:
    #     tmp = arr[x, y]
    #     arr[x, y] = '*'
    #     print(arr)
    #     arr[x, y] = tmp
    # does the path stack contain a right angle?
    count = 0
    for i in range(len(path_stack) - 2):
        p1 = path_stack[i]
        p2 = path_stack[i+1]
        p3 = path_stack[i+2]
        if is_right_angle(p1, p2, p3):
            tmp1, tmp2, tmp3 = arr[p1], arr[p2], arr[p3]
            arr[p1] = '*'
            arr[p2] = '*'
            arr[p3] = '*'
            print(arr)
            arr[p1] = tmp1
            arr[p2] = tmp2
            arr[p3] = tmp3
            count += 1

    # the last two points
    p1 = path_stack[-2]
    p2 = path_stack[-1]
    p3 = path_stack[0]
    if is_right_angle(p1, p2, p3):
        count += 1
    
    p1 = path_stack[-1]
    p2 = path_stack[0]
    p3 = path_stack[1]
    if is_right_angle(p1, p2, p3):
        count += 1
    
    return count

# def count_adjecent_sides_helper(arr, x, y, dx, dy, perimeters, region, vperimeter=None):
#     if not vperimeter:
#         vperimeter = set()
#     tmp = arr[x, y]
#     arr[x, y] = '*'
#     print(arr)
#     arr[x, y] = tmp
#     if len(vperimeter) == len(perimeters):
#         return 0
#     if (x+dx, y+dy) not in perimeters:
#         ccw_dx, ccw_dy = rotate_90_degrees_ccw((dx, dy))
#         cw_dx, cw_dy = rotate_90_degrees_cw((dx, dy))
#         return min(
#             1 + count_adjecent_sides_helper(arr, x, y, ccw_dx, ccw_dy, perimeters, region, vperimeter | {(x, y)}),
#             1 + count_adjecent_sides_helper(arr, x, y, cw_dx, cw_dy, perimeters, region, vperimeter | {(x, y)})
#         )
#     return count_adjecent_sides_helper(arr, x+dx, y+dy, dx, dy, perimeters, region, vperimeter | {(x, y)})

def find_all_corners(arr, region, l):
    # if len(region) < 4:
    #     return 4
    x_min, y_min = min(region, key=lambda x: x[0])[0], min(region, key=lambda x: x[1])[1]
    x_max, y_max = max(region, key=lambda x: x[0])[0], max(region, key=lambda x: x[1])[1]
    tmp_arr = arr[x_min:x_max+1, y_min:y_max+1].copy()
    for i in range(tmp_arr.shape[0]):
        for j in range(tmp_arr.shape[1]):
            if (x_min + i, y_min + j) not in region:
               tmp_arr[i, j] = 0
            else:
                tmp_arr[i, j] = 1
    tmp_arr = np.pad(tmp_arr, 2, 'constant', constant_values=0).astype(int)
    # print(tmp_arr)
    corners = 0
    # print(tmp_arr)
    for i in range(1, tmp_arr.shape[0] - 1):
        for j in range(1, tmp_arr.shape[1] - 1):
            corners += is_corner(tmp_arr[i-1:i+1, j-1:j+1])
    return corners
    

def count_adjecent_sides(arr, perimeters, current_region):
    # remove the regions that are standalone
    revisied_perimeters = set()
    for x, y in perimeters:
        if not get_straight_options(arr, x, y, perimeters, set()):
            if not get_adjecent_sides(arr, x, y, perimeters, set()):
                revisied_perimeters.add((x, y))
    count = 4 * len(revisied_perimeters)
    x, y = (perimeters - revisied_perimeters).pop()
    _, _, dx, dy = get_straight_options(arr, x, y, perimeters, set())[0]
    return count + count_adjecent_sides_helper(arr, x, y, dx, dy, perimeters - revisied_perimeters, current_region)



def part_one():
    p1data = data
    arr = np.array([list(row) for row in p1data.split('\n') if row])
    unique = np.unique(arr)
    visited_per_letter = {
        v: set() for v in unique
    }
    total_cost = 0
    for v in unique:
        locations = [(x,y) for x, y in np.argwhere(arr == v)]
        while locations:
            x, y = locations.pop()
            curr_area = len(visited_per_letter[v])
            curr_visited = copy.deepcopy(visited_per_letter[v])
            perimeters = traverse_letter(arr, x, y, v, visited_per_letter)
            new_visited = visited_per_letter[v] - curr_visited
            perimeter_count = count_perimeters(perimeters, new_visited)
            area_delta = len(visited_per_letter[v]) - curr_area
            total_cost += area_delta * perimeter_count
            locations = set(locations) - visited_per_letter[v]
            locations = list(locations)
            # print(f"Area: {area_delta}, Perimeter: {perimeter_count}, Total Cost: {total_cost}")
    print(total_cost)

def part_two():
    p2data = data
    arr = np.array([list(row) for row in p2data.split('\n') if row])
    arr = np.pad(arr, 1, 'constant', constant_values='.')
    unique = np.unique(arr)
    unique = unique[unique != '.']
    visited_per_letter = {
        v: set() for v in unique
    }
    total_cost = 0
    for v in unique:
        # if v != 'E':
        #     continue
        locations = [(x,y) for x, y in np.argwhere(arr == v)]
        print('Letter:', v)
        while locations:
            x, y = locations.pop()
            curr_area = len(visited_per_letter[v])
            curr_visited = copy.deepcopy(visited_per_letter[v])
            perimeters = traverse_letter_v2(arr, x, y, v, visited_per_letter)
            current_region = visited_per_letter[v] - curr_visited
            # side_count = count_adjecent_sides(arr, perimeters, current_region)
            side_count = find_all_corners(arr, current_region, v)
            area_delta = len(visited_per_letter[v]) - curr_area
            total_cost += area_delta * side_count
            locations = set(locations) - visited_per_letter[v]
            locations = list(locations)
            print(f"Area: {area_delta}, Side Count: {side_count}, Cost: {area_delta * side_count}")
    print(total_cost)

# part_one()
part_two()