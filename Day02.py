from Utility import *

filePath = 'input/day02/part1.txt'


def solvePart1():
    inputLines = getLinesFromFile(filePath)
    x, y = 0, 0
    for line in inputLines:
        if(line.startswith('forward')):
            x += int(line.split(' ')[1])
        if(line.startswith('down')):
            y += int(line.split(' ')[1])
        if(line.startswith('up')):
            y -= int(line.split(' ')[1])
    result = x * y

    print('Solution to part1:')
    print(result)


def solvePart2():
    inputLines = getLinesFromFile(filePath)
    x, y, aim = 0, 0, 0
    for line in inputLines:
        value = int(line.split(' ')[1])

        if(line.startswith('forward')):
            x += value
            y += aim * value
        if(line.startswith('down')):
            aim += value
        if(line.startswith('up')):
            aim -= value
    result = x * y

    print('Solution to part2:')
    print(result)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
