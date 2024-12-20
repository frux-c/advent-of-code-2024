import readfile
import copy

data = readfile.read_day_file(11).strip()

test_data = "125 17"

def part_one():
    p1data = data
    arr = list(map(int, p1data.split(' ')))
    blinks = 75
    for _ in range(blinks):
        new_arr = []
        for i in range(len(arr)):
            if arr[i] == 0:
                new_arr.append(1)
            elif len(str(arr[i])) & 1 == 0:
                left_digit, right_digit = str(arr[i])[:len(str(arr[i]))//2], str(arr[i])[len(str(arr[i]))//2:]
                new_arr.append(int(left_digit))
                new_arr.append(int(right_digit))
            else:
                new_arr.append(arr[i] * 2024)
        arr = copy.deepcopy(new_arr)
        del new_arr
    # print(arr)
    print(len(arr))

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

def part_two():
    p2data = data
    blinks = 75
    _map = {k: 1 for k in map(int, p2data.split(' '))}
    for _ in range(blinks):
        new_map = {}
        for k, v in _map.items():
            if k == 0:
                new_map[1] = new_map.get(1, 0) + v
            elif len(str(k)) & 1 == 0:
                left, right = int(str(k)[:len(str(k))//2]), int(str(k)[len(str(k))//2:])
                new_map[left] = new_map.get(left, 0) + v
                new_map[right] = new_map.get(right, 0) + v
            else:
                new_map[k * 2024] = new_map.get(k * 2024, 0) + v
        _map = new_map
    print(sum(_map.values()))
part_two()