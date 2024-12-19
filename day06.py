import readfile
import numpy as np
import copy
import time
import threading
import queue
import multiprocessing as mp

data = readfile.read_day_file(6)

test_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

def part_one():
    p1data = copy.deepcopy(data).strip()
    arr = np.array([[col for col in row] for row in p1data.split('\n')], dtype=str)
    direction_list = ['^', '>', 'v', '<']
    direction = {
        '^': np.array((-1, 0)),
        'v': np.array((1, 0)),
        '<': np.array((0, -1)),
        '>': np.array((0, 1))
    }
    current_location = np.array((0, 0))
    current_direction = np.array((0, 0))
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j] in direction:
                current_location = np.array((i, j))
                current_direction = direction[arr[i, j]]
                break
    while True:
        next_location = current_location + current_direction
        if next_location[0] < 0 or next_location[0] >= arr.shape[0] or next_location[1] < 0 or next_location[1] >= arr.shape[1]:
            arr[current_location[0], current_location[1]] = 'X'
            break
        if arr[next_location[0], next_location[1]] == '#':
            # rotate 90 degrees
            next_direction = (direction_list.index(arr[current_location[0], current_location[1]]) + 1) % 4
            arr[current_location[0], current_location[1]] = direction_list[next_direction]
            current_direction = direction[direction_list[next_direction]]
        else:
            arr[next_location[0], next_location[1]] = arr[current_location[0], current_location[1]]
            arr[current_location[0], current_location[1]] = 'X'
            current_location = next_location
    print(sum(sum(arr == 'X')))


def play_game(arr, current_location, current_direction):
    direction_list = ['^', '>', 'v', '<']
    direction = {
        '^': np.array((-1, 0)),
        'v': np.array((1, 0)),
        '<': np.array((0, -1)),
        '>': np.array((0, 1))
    }
    st = time.perf_counter()
    timeout = False
    while not timeout:
        dt = time.perf_counter() - st
        if dt > 2:
            timeout = True
        next_location = current_location + current_direction
        if next_location[0] < 0 or next_location[0] >= arr.shape[0] or next_location[1] < 0 or next_location[1] >= arr.shape[1]:
            arr[current_location[0], current_location[1]] = 'X'
            break
        if arr[next_location[0], next_location[1]] == '#':
            # rotate 90 degrees
            next_direction = (direction_list.index(arr[current_location[0], current_location[1]]) + 1) % 4
            arr[current_location[0], current_location[1]] = direction_list[next_direction]
            current_direction = direction[direction_list[next_direction]]
        else:
            arr[next_location[0], next_location[1]] = arr[current_location[0], current_location[1]]
            arr[current_location[0], current_location[1]] = 'X'
            current_location = next_location
    return 1 if timeout else 0

def part_two():
    p2data = copy.deepcopy(data).strip()
    arr2 = np.array([[col for col in row] for row in p2data.split('\n')], dtype=str)
    direction_list = ['^', '>', 'v', '<']
    direction = {
        '^': np.array((-1, 0)),
        'v': np.array((1, 0)),
        '<': np.array((0, -1)),
        '>': np.array((0, 1))
    }
    original_current_location = np.array((0, 0))
    original_current_direction = np.array((0, 0))
    for i in range(arr2.shape[0]):
        for j in range(arr2.shape[1]):
            if arr2[i, j] in direction:
                original_current_location = np.array((i, j))
                original_current_direction = direction[arr2[i, j]]
                break
    original_arr = copy.deepcopy(arr2)
    futures = []
    count_queue = queue.Queue()
    pool = mp.Pool(mp.cpu_count())
    for i in range(arr2.shape[0]):
        for j in range(arr2.shape[1]):
            if original_current_location[0] == i and original_current_location[1] == j:
                continue
            arr = copy.deepcopy(original_arr)
            current_location = copy.deepcopy(original_current_location)
            current_direction = copy.deepcopy(original_current_direction)
            arr[i, j] = '#'
            futures.append(pool.apply_async(play_game, args=(arr, current_location, current_direction)))
    while True:
        if all(future.ready() for future in futures):
            break
    print(sum((future.get() for future in futures)))
#             def game():
#                 arr = copy.deepcopy(original_arr)
#                 current_location = copy.deepcopy(original_current_location)
#                 current_direction = copy.deepcopy(original_current_direction)
#                 arr[i, j] = '#'
#                 st = time.perf_counter()
#                 timeout = False
#                 while not timeout:
#                     dt = time.perf_counter() - st
#                     if dt > 10:
#                         timeout = True
#                     next_location = current_location + current_direction
#                     if next_location[0] < 0 or next_location[0] >= arr.shape[0] or next_location[1] < 0 or next_location[1] >= arr.shape[1]:
#                         arr[current_location[0], current_location[1]] = 'X'
#                         break
#                     if arr[next_location[0], next_location[1]] == '#':
#                         # rotate 90 degrees
#                         next_direction = (direction_list.index(arr[current_location[0], current_location[1]]) + 1) % 4
#                         arr[current_location[0], current_location[1]] = direction_list[next_direction]
#                         current_direction = direction[direction_list[next_direction]]
#                     else:
#                         arr[next_location[0], next_location[1]] = arr[current_location[0], current_location[1]]
#                         arr[current_location[0], current_location[1]] = 'X'
#                         current_location = next_location
#                 if timeout:
#                     if not count_queue.empty():
#                         count_queue.put(1 + count_queue.get())
#                     else:
#                         count_queue.put(1)
#             thread = threading.Thread(target=game)
#             thread.start()
#             print(thread)
#             threads.append(thread)
#     count = 0
#     while True:
#         if all(not thread.is_alive() for thread in threads):
#             break
#     print('all threads stopped')
#     while not count_queue.empty():
#         print('counting')
#         count += count_queue.get()
#     print(count)
# # part_one()
if __name__ == '__main__':
    part_two()