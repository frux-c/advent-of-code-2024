import readfile
import numpy as np
import copy


data = readfile.read_day_file(1)
data = np.array([x.split() for x in data.split('\n') if x], dtype=int).T

def partOne():
	data_copy = copy.deep_copy(data)
	for i in range(data_copy.shape[0]):
		data[i] = np.sort(data_copy[i])

	distance = np.abs(data_copy[0] - data_copy[1])

	answer = distance.sum()

	print(answer)

def partTwo():
	data_copy = copy.deep_copy(data)
	unique_val, counts = np.unique(data_copy[1], return_counts=True)
	count_map = dict(zip(unique_val, counts))

	for i, num in enumerate(data[0]):
		data_copy[0][i] = data_copy[0][i] * count_map.get(num, 0)

	answer = np.sum(data_copy[0])

	print(answer)
