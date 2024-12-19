import readfile
import re
import copy

data = readfile.read_day_file(3)

def mul(a, b):
	return a * b

def part_one():
	p1_data = copy.deepcopy(data)
	pattern = re.compile(r"mul\(\d+,\d+\)")
	result = pattern.findall(p1_data)
	s = 0
	for r in result:
		s += eval(r)

	print(s)


def part_two():
	p2_data = copy.deepcopy(data)
	pattern = re.compile(r"mul\(\d+,\d+\)")
	result = re.finditer(pattern, p2_data)
	do_pattern = re.compile(r"do(n't)?\(\)")
	result2 = re.finditer(do_pattern, p2_data)
	resultt = sorted(list(result) + list(result2), key=lambda x: x.start())
	s = 0
	active = True
	for r in resultt:
		if r.group().startswith("don't"):
			active = False
			continue
		elif r.group() == "do()":
			active = True
			continue
		if active:
			s += eval(r.group())
	print(s)
	
# part_one()
part_two()