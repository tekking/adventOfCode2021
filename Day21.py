import Utility

filePath = 'input/day21/part1.txt'

def getStartingPositions() -> tuple[int, int]:
    inputLines = Utility.getLinesFromFile(filePath)
    playerOneStart = int(inputLines[0].split(' ')[-1])
    playerTwoStart = int(inputLines[1].split(' ')[-1])
    return (playerOneStart, playerTwoStart)

def getDiracDistribution() -> list[tuple[int, int]]:
    distribution = {}
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                total = d1 + d2 + d3
                existingValue = distribution.get(total, 0)
                distribution.update({total: existingValue + 1})
    return list(distribution.items())


def solvePart1():
    p1, p2 = getStartingPositions()

    p1Score, p2Score = 0,0
    nextRoll = 1
    totalRolls = 0

    while(p1Score < 1000 and p2Score < 1000):
        if (totalRolls % 2 == 0):
            p1 = ((p1 - 1 + nextRoll + nextRoll + 1 + nextRoll + 2) % 10) + 1
            p1Score += p1
        else:
            p2 = ((p2 - 1 + nextRoll + nextRoll + 1 + nextRoll + 2) % 10) + 1
            p2Score += p2
        
        totalRolls += 3
        nextRoll = (nextRoll + 2 % 100) + 1

    loserScore = p1Score if p1Score < p2Score else p2Score 

    print('Solution to part1:')
    print(loserScore * totalRolls)
    print()


def solvePart2():
    p1Start, p2Start = getStartingPositions()
    diracDistribution = getDiracDistribution()

    p1Universes, p2Universes = 0, 0

    totalRolls = 0

    # represented as (p1 position, p2 position, p1 score, p2 score) : # universes
    distribution = {(p1Start, p2Start, 0, 0): 1}

    while(len(list(distribution.items())) > 0):
        print(len(list(distribution.items())))
        newDistribution = {}
        for (p1, p2, p1Score, p2Score) , universes in distribution.items():
            for score, nrOfRolls in diracDistribution:
                if totalRolls % 2 == 0:
                    newP1 = ((p1 - 1 + score) % 10) + 1
                    newP1Score = p1Score +  newP1
                    if newP1Score >= 21:
                        p1Universes += universes * nrOfRolls
                    else:
                        repr = (newP1, p2, newP1Score, p2Score)
                        existingValue = newDistribution.get(repr, 0)
                        newDistribution.update({repr: existingValue + universes * nrOfRolls})
                else:
                    newP2 = ((p2 - 1 + score) % 10) + 1
                    newP2Score = p2Score + newP2
                    if newP2Score >= 21:
                        p2Universes += universes * nrOfRolls
                    else:
                        repr = (p1, newP2, p1Score, newP2Score)
                        existingValue = newDistribution.get(repr, 0)
                        newDistribution.update({repr: existingValue + universes * nrOfRolls})
                
        totalRolls += 1
        distribution = newDistribution

    print('Solution to part2:')
    print(p1Universes)
    print(p2Universes)

if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
