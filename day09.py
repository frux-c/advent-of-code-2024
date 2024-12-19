import readfile
import re

data = readfile.read_day_file(9).strip()

test_data = "2333133121414131402"

def part_one():
    p1data = data
    arr = []
    s = 0
    for i in range(len(p1data)):
        if i & 1:
            arr += [None] * int(p1data[i])
        else:
            arr += [s] * int(p1data[i])
            s += 1

    left_ptr = 0
    # print(arr)
    while left_ptr < len(arr):
        if arr[left_ptr] == None:
            for i in range(len(arr)-1, left_ptr, -1):
                if arr[i] != None:
                    arr[left_ptr] = arr[i]
                    arr[i] = None
                    break
        left_ptr += 1
    
    # print(arr)
    _sum = 0
    for i, v in enumerate(arr):
        if v is None:
            break
        _sum += i * v
    print(_sum)

def part_two():
    p2data = data
    arr = []
    s = 0
    for i in range(len(p2data)):
        # save a tuple (is_space, repeat_count)
        if i & 1:
            arr.append((True, None, int(p2data[i])))
        else:
            arr.append((False, s, int(p2data[i])))
            s += 1
    
    s -= 1
    
    while s >= 0:
        for i in range(len(arr)-1, -1, -1):
            is_space, v, repeat_count = arr[i]
            if is_space or not v or v != s:
                continue
            for j in range(i):
                is_space2, v2, repeat_count2 = arr[j]
                if not is_space2:
                    pass
                elif repeat_count2 == repeat_count:
                    arr = arr[:j] + [(False, s, repeat_count)] + arr[j+1:i] + [(True, None, repeat_count)] + arr[i+1:]
                    break
                elif repeat_count2 > repeat_count:
                    arr = arr[:j] + [(False, s, repeat_count)] + [(True, None, repeat_count2 - repeat_count)] + arr[j+1:i] + [(True, None, repeat_count)] + arr[i+1:]
                    break
                    
        s -= 1
    # print(arr)
    # join array into a string
    # s = ""
    # for is_space, v, repeat_count in arr:
    #     if is_space:
    #         s += "." * repeat_count
    #     else:
    #         s += str(v) * repeat_count
    # print(s)
    i = 0
    _sum = 0
    for v in arr:
        is_space, val, repeat_count = v
        if is_space:
            i += repeat_count
            continue
        for _ in range(repeat_count):
            _sum += i * val
            i += 1
    print(_sum)
part_two()