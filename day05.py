from readfile import read_day_file
import copy

data = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def topologicalSortUtil(v, adj, visited, stack):
    # Mark the current node as visited
    visited[v] = True

    # Recur for all adjacent vertices
    for i in adj[v]:
        if not visited[i]:
            topologicalSortUtil(i, adj, visited, stack)

    # Push current vertex to stack which stores the result
    stack.append(v)


# Function to perform Topological Sort
def topologicalSort(adj, V):
    # Stack to store the result
    stack = []

    visited = [False] * V

    # Call the recursive helper function to store
    # Topological Sort starting from all vertices one by
    # one
    for i in range(V):
        if not visited[i]:
            topologicalSortUtil(i, adj, visited, stack)

    # Print contents of stack
    # print("Topological sorting of the graph:", end=" ")
    # while stack:
    #     print(stack.pop(), end=" ")
    return [stack.pop() for _ in range(len(stack))]

data = read_day_file(5).strip()

class OrderedSet:
    def __init__(self):
        self.data = dict()
    
    def add(self, item):
        self.data[item] = len(self.data)
    
    def __contains__(self, item):
        return item in self.data
    
    def __len__(self):
        return len(self.data)
    
    def __iter__(self):
        return dict.fromkeys(self.data)
    

def part_one_v2():
    p1_data = copy.deepcopy(data)
    rules, items = p1_data.split('\n\n')
    rules = rules.split('\n')
    items = items.split('\n')
    items = [list(map(int,item.split(','))) for item in items]
    rules = [tuple(map(int,rule.split('|'))) for rule in rules]
    rule_dict = dict()
    for rule in rules:
        pred, succ = rule
        if pred not in rule_dict:
            rule_dict[pred] = set([succ])
        else:
            rule_dict[pred].add(succ)
    
    answer = 0
    for item in items:
        bad_update = False
        for i in range(len(item)-1, 0, -1):
            if set(item[:i]).intersection(rule_dict.get(item[i], set())):
                bad_update = True
                break
        if not bad_update:
            mid = len(item) // 2
            answer += item[mid]
    print(answer)

def reorder_item(item, rules: dict):
    for i in range(len(item)):
        for j in range(i + 1, len(item)):
            if item[j] in rules.get(item[i], set()):
                item[i], item[j] = item[j], item[i]

def part_two():
    p1_data = copy.deepcopy(data)
    rules, items = p1_data.split('\n\n')
    rules = rules.split('\n')
    items = items.split('\n')
    items = [list(map(int,item.split(','))) for item in items]
    rules = [tuple(map(int,rule.split('|'))) for rule in rules]
    rule_dict = dict()
    for rule in rules:
        pred, succ = rule
        if pred not in rule_dict:
            rule_dict[pred] = set([succ])
        else:
            rule_dict[pred].add(succ)
    individual_rule = set()
    for rule in rules:
        individual_rule = individual_rule.union(rule)
    individual_rule = list(individual_rule)
    V = len(individual_rule)
    adj = [[] for _ in range(V)]
    for rule in rules:
        pred, succ = rule
        adj[individual_rule.index(pred)].append(individual_rule.index(succ))
    ret = topologicalSort(adj, V)
    print([individual_rule[i] for i in ret])
    ordered_set = {individual_rule[i]: k for k, i in enumerate(ret)}
    answer = 0
    for item in items:
        bad_update = False
        for i in range(len(item)-1, 0, -1):
            if set(item[:i]).intersection(rule_dict.get(item[i], set())):
                bad_update = True
                break
        if bad_update:
            reorder_item(item, rule_dict)
            mid = len(item) // 2
            answer += item[mid]
    print(answer)

def part_one():
    p1_data = copy.deepcopy(data)
    rules, items = p1_data.split('\n\n')
    rules = rules.split('\n')
    items = items.split('\n')
    rules = [tuple(map(int,rule.split('|'))) for rule in rules]
    individual_rule = set()
    # ordering = dict()
    for rule in rules:
        individual_rule = individual_rule.union(rule)
    individual_rule = list(individual_rule)
    V = len(individual_rule)
    adj = [[] for _ in range(V)]
    for rule in rules:
        pred, succ = rule
        adj[individual_rule.index(pred)].append(individual_rule.index(succ))
    ret = topologicalSort(adj, V)
    # print(ret)
    # print("sorted_rules", sorted_rules)
    # print(adj)
    # print(individual_rule)
    # for rule in rules:
    #     pred, succ = rule
    #     if pred not in ordering:
    #         ordering[pred] = set([succ])
    #     else:
    #         ordering[pred].add(succ)
    # for i, r in enumerate(individual_rule):
    #     if r not in ordering:
    #         continue
    #     pred_slice = individual_rule[:i]
    #     for k, pred in enumerate(pred_slice):
    #         if pred in ordering[r]:
    #             individual_rule[i], individual_rule[k] = individual_rule[k], individual_rule[i]
    #         # if pred in ordering[r]:
    #         #     individual_rule.append(individual_rule.pop(k))
    #     # print(individual_rule)
    # # print(individual_rule)
    # # print()
    # print([individual_rule[i] for i in ret])
    ordered_set = {individual_rule[i]: k for k, i in enumerate(ret)}
    items = [list(map(int,item.split(','))) for item in items]

    answer = 0
    for item in items:
        is_in_order = [ordered_set[val] for val in item if val in ordered_set]
        is_in_order_true = True
        for l in range(len(is_in_order[:-1])):
            if is_in_order[l] > is_in_order[l+1]:
                is_in_order_true = False
                print("i broke at", is_in_order[l], is_in_order[l+1])
                break
        if is_in_order_true:
            mid = len(item) // 2
            answer += item[mid]
        
    print(answer)
# part_one_v2()
part_two()