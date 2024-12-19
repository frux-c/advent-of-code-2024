import readfile
import copy
import numpy as np

data = readfile.read_day_file(2)

data = [list(map(int, x.split())) for x in data.split("\n") if x]

def part_one():
	r, c = len(data), max([len(x) for x in data])
	safe_count = 0
	for i, x in enumerate(data):
		is_asc = x[1] - x[0] > 0
		safe = 1
		for j, y in enumerate(x[:-1]):
			diff = x[j+1] - y
			if not (is_asc ^ (diff < 0)):
				# print(is_asc, diff)
				safe = 0
				break
			elif not (-3 <= diff <= 3) or diff == 0:
				safe = 0
				break
		safe_count += safe
	
	print(safe_count)

def part_two():
	r, c = len(data), max([len(x) for x in data])
	safe_count = 0
	for i, x in enumerate(data):
		is_asc = x[1] - x[0] > 0
		safe = 1
		for j, y in enumerate(x[:-1]):
			diff = x[j+1] - y
			if not (is_asc ^ (diff < 0)):
				safe = 0
				break
			elif not (-3 <= diff <= 3) or diff == 0:
				safe = 0
				break
		if safe == 0:
			for k in range(len(x)):
				z = [w for f, w in enumerate(x) if f != k]
				is_asc = z[1] - z[0] > 0
				safe2 = 1
				for l, m in enumerate(z[:-1]):
					diff = z[l+1] - m
					if not (is_asc ^ (diff < 0)):
						safe2 = 0
						break
					elif not (-3 <= diff <= 3) or diff == 0:
						safe2 = 0
						break
				if safe2 == 1:
					safe = 1
					break
		safe_count += safe

	print(safe_count)
	
part_two()
