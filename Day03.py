import Utility

part1FilePath = 'input/day03/part1.txt'


def findMostCommonBit(inputLines, index):
    total = sum(map(lambda x: int(x[index]), inputLines))
    if (total * 2 >= len(inputLines)):
        return '1'
    else:
        return '0'


def solvePart1():
    inputLines = Utility.getLinesFromFile(part1FilePath)
    gamma, epsilon = 0, 0

    mostCommonBits = ''
    leastCommonBits = ''
    for i in range(len(inputLines[0])):
        if findMostCommonBit(inputLines, i) == '1':
            mostCommonBits += '1'
            leastCommonBits += '0'
        else:
            mostCommonBits += '0'
            leastCommonBits += '1'

    gamma = int(mostCommonBits, 2)
    epsilon = int(leastCommonBits, 2)

    print('Solution to part1:')
    print(gamma * epsilon)


def solvePart2():
    inputLines = Utility.getLinesFromFile(part1FilePath)
    oxygen, co2 = 0, 0
    oxygenLines = inputLines.copy()
    co2Lines = inputLines.copy()

    oxygenIndex = 0
    while(len(oxygenLines) > 1):
        mostCommonBit = findMostCommonBit(oxygenLines, oxygenIndex)
        oxygenLines = list(
            filter(lambda n: n[oxygenIndex] == mostCommonBit, oxygenLines))
        oxygenIndex += 1

    co2Index = 0
    while(len(co2Lines) > 1):
        mostCommonBit = findMostCommonBit(co2Lines, co2Index)
        co2Lines = list(
            filter(lambda n: n[co2Index] != mostCommonBit, co2Lines))
        co2Index += 1

    oxygen = int(oxygenLines[0], 2)
    co2 = int(co2Lines[0], 2)

    print('Solution to part2:')
    print(oxygen * co2)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
