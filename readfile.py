
def read_day_file(day: int):
	with open(f"data/day{day:02}.txt", 'r') as f:
		data = f.read()
	return data