from Utility import *

part1FilePath = 'input/day01/part1.txt'


def solvePart1():
    inputLines = getLinesFromFile(part1FilePath)
    values = list(map(int, inputLines))
    numberOfIncreases = 0
    for i, line in enumerate(values[1:]):
        if (line > values[i]):
            numberOfIncreases += 1
    print('Solution to part1:')
    print(numberOfIncreases)


def solvePart2():
    inputLines = getLinesFromFile(part1FilePath)
    values = list(map(int, inputLines))

    def calculateSlidingWindow(index):
        return sum(values[index:index+3])

    numberOfIncreases = sum(map(lambda i: 1 if calculateSlidingWindow(
        i) > calculateSlidingWindow(i-1) else 0, range(1, len(values)-2)))
    print('Solution to part2:')
    print(numberOfIncreases)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
