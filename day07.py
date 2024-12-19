import readfile
import copy
import functools
data = readfile.read_day_file(7)

test_data = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def part_one():
    p1data = copy.deepcopy(data).strip()
    collections = []
    for line in p1data.splitlines():
        line = line.split(': ')
        collections.append(
            (int(line[0]), 
             list(map(int, line[1].split(' ')))
        ))
    def can_add_or_multiply(goal_value, collection, current_value=0):
        if current_value and current_value == goal_value:
            return True
        if not collection:
            return False
        if current_value is None and len(collection) >= 2:
            return can_add_or_multiply(goal_value, collection[2:], collection[0] + collection[1]) or \
            can_add_or_multiply(goal_value, collection[2:], collection[0] * collection[1])
        else:
            return can_add_or_multiply(goal_value, collection[1:], collection[0] + current_value) or \
            can_add_or_multiply(goal_value, collection[1:], collection[0] * current_value)
    answer = 0
    for collection in collections:
        if can_add_or_multiply(collection[0], collection[1]):
            answer += collection[0]
    print(answer)


def part_two():
    p2data = copy.deepcopy(data).strip()
    collections = []
    for line in p2data.splitlines():
        line = line.split(': ')
        collections.append(
            (int(line[0]), 
             list(map(int, line[1].split(' ')))
        ))
    def can_add_or_multiply_or_concat(goal_value, collection):
        if collection[0] > goal_value:
            return False
        if len(collection) == 1 and collection[0] == goal_value:
            return True
        if len(collection) >= 2:
            return \
            can_add_or_multiply_or_concat(goal_value, [collection[0] + collection[1]] + collection[2:]) or \
            can_add_or_multiply_or_concat(goal_value, [collection[0] * collection[1]] + collection[2:]) or \
            can_add_or_multiply_or_concat(goal_value, [int(str(collection[0]) + str(collection[1]))] + collection[2:])
    answer = 0
    for collection in collections:
        if can_add_or_multiply_or_concat(collection[0], collection[1]):
            answer += collection[0]
    print(answer)
# part_one()
part_two()

"""
def can_add_or_multiply_or_concat(goal_value, collection):
    stack = [(collection, 0, 0)]
    while stack:
        current_collection, current_index, current_value = stack.pop()
        if current_value and current_value == goal_value:
            return True
        if current_index >= len(current_collection):
            continue
        if current_value is None and current_index + 1 < len(current_collection):
            stack.append((current_collection, current_index + 2, current_collection[current_index] + current_collection[current_index + 1]))
            stack.append((current_collection, current_index + 2, current_collection[current_index] * current_collection[current_index + 1]))
            stack.append((current_collection, current_index + 2, int(str(current_collection[current_index]) + str(current_collection[current_index + 1]))))
        else:
            stack.append((current_collection, current_index + 1, current_collection[current_index] + current_value))
            stack.append((current_collection, current_index + 1, current_collection[current_index] * current_value))
            stack.append((current_collection, current_index + 1, int(str(current_collection[current_index]) + str(current_value))))
    return False
"""