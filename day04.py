import readfile
import re
import copy
import numpy as np

data = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()
data = readfile.read_day_file(4).strip()

def part_one():
	def find_xmas(grid, x, y, word):
	    equals_word = lambda v: int(''.join(v) == word) + int(''.join(v) == word[::-1])
	    n = len(word)
	    count = 0
	    coor = set()

	    # backwards
	    if 0 <= y - n + 1 and y < len(grid[x]):
	        res = equals_word([grid[x][y-i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x, y-i))

	    # forward
	    if y + n <= len(grid[x]):
	        res = equals_word([grid[x][y+i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x, y+i))

	    # up
	    if 0 <= x - n + 1 and x < len(grid):
	        res = equals_word([grid[x-i][y] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x-i, y))

	    # down
	    if x + n <= len(grid):
	        res = equals_word([grid[x+i][y] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x+i, y))

	    # diagonal dn + fw
	    if x + n <= len(grid) and y + n <= len(grid[x]):
	        res = equals_word([grid[x+i][y+i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x+i, y+i))

	    # diagonal up + fw
	    if 0 <= x - n + 1 and y + n <= len(grid[x]):
	        res = equals_word([grid[x-i][y+i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x-i, y+i))

	    # diagonal dn + bw
	    if x + n <= len(grid) and 0 <= y - n + 1:
	        res = equals_word([grid[x+i][y-i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x+i, y-i))

	    # diagonal up + bw
	    if 0 <= x - n + 1 and 0 <= y - n + 1:
	        res = equals_word([grid[x-i][y-i] for i in range(n)])
	        count += res
	        if res:
	            for i in range(n):
	                coor.add((x-i, y-i))

	    return coor, count
	p1_data = np.array([[l for l in row] for row in data.split('\n')])
	total_count = 0
	tcore = set([(x,y) for x in range(p1_data.shape[0]) for y in range(p1_data.shape[1])])
	# print(tcore)
	for x in range(len(p1_data)):
		for y in range(len(p1_data[x])):
			if p1_data[x][y] == 'X':
				coor, count = find_xmas(p1_data, x, y, 'XMAS')
				tcore -= coor
				total_count += count
	# print(tcore)
	print(total_count)
	for x, y in tcore:
		p1_data[x,y] = '.'
	new_data = '\n'.join([''.join(row) for row in p1_data])
	print(new_data)

def part_two():
	def find_xmas(grid, x, y):
		if not (0 <= x - 1 < len(grid) and \
		   0 <= x + 1 < len(grid) and \
		   0 <= y - 1 < len(grid[x]) and \
		   0 <= y + 1 < len(grid[x])):
			return 0
		w1 = grid[x-1,y-1] + grid[x,y] + grid[x+1,y+1]
		w2 = grid[x+1,y-1] + grid[x,y] + grid[x-1,y+1]
		return (w1 == "MAS" or w1[::-1] == "MAS") and (w2 == "MAS" or w2[::-1] == "MAS")


	p2_data = np.array([[l for l in row] for row in data.split('\n')])
	total_count = 0
	for x in range(p2_data.shape[0]):
		for y in range(p2_data.shape[1]):
			if p2_data[x,y] == 'A':
				total_count += find_xmas(p2_data, x, y)
	print(total_count)

part_two()
# part_one()

