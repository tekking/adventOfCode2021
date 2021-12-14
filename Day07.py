from os import popen
import Utility

filePath = 'input/day07/part1.txt'

def getHorizontalPositions():
    inputLines = Utility.getLinesFromFile(filePath)
    return list(map(int, inputLines[0].split(',')))


def solvePart1():
    positions = getHorizontalPositions()

    sortedPositions = sorted(positions)
    optimalPosition = sortedPositions[len(sortedPositions)//2]

    maxValue = max(positions)
    spread = [0 for i in range(maxValue + 1)]
    for i in positions:
        spread[i] += 1
    
    score = 0
    for n in range(maxValue + 1):
        score += abs(optimalPosition - n) * spread[n]

    print('Solution to part1:')
    print(optimalPosition)
    print(score)


def calculateCost(start, end):
    diff = abs(start - end)
    return diff * (diff + 1) / 2


def solvePart2():
    positions = getHorizontalPositions()
    
    maxValue = max(positions)
    spread = [0 for i in range(maxValue + 1)]
    for i in positions:
        spread[i] += 1

    bestScore = len(positions) * (maxValue**2)
    bestValue = 0
    for i in range(maxValue + 1):
        score = 0
        for n in range(maxValue + 1):
            score += calculateCost(i, n) * spread[n]
        if (score < bestScore):
            bestScore = score
            bestValue = i

    print('Solution to part2:')
    print(bestValue)
    print(bestScore)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
