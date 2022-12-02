from functools import reduce

def _load_file():
	# Open the file in read-only mode
	return open('data/01.txt', 'r')

def _getRations():
	f = _load_file()
	elves = list()
	currentElf = list()
	for line in f:
		if line == '\n':
			elves.append(currentElf)
			currentElf = list()
		else:
			currentElf.append(int(line.strip('\n')))
	elves.append(currentElf)
	calories = list(map(lambda l: reduce(lambda a, b: a+b, l), elves))
	calories.sort()
	return calories

def _part1():
	return _getRations()[-1]

def _part2():
	return sum(_getRations()[-3:])

def main():
	return _part1(), _part2()
