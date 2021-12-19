import Utility

filePath = 'input/day17/part1.txt'

class Target:
    def __init__(self) -> None:
        inputlines = Utility.getLinesFromFile(filePath)
        line = inputlines[0]
        parts = line.split(' ')
        xPart = parts[2]
        yPart = parts[3]
        self.xMin, self.xMax = list(map(int, xPart.split(',')[0].split('=')[1].split('..')))
        self.yMin, self.yMax = list(map(int, yPart.split(',')[0].split('=')[1].split('..')))


def calculatePathForLaunch(xV, yV, maxDepth) -> list[tuple[int, int]]:
    x, y = 0, 0
    positions = []
    while(y >= maxDepth):
        x += xV
        y += yV
        positions.append((x, y))
        if xV > 0:
            xV -= 1
        yV -= 1
    return positions

def launchHitsTargetWithHighestPoint(target: Target, xV, yV) -> tuple[bool, int]:
    positions = calculatePathForLaunch(xV, yV, target.yMin)

    for p in positions:
        if (p[0] >= target.xMin and p[0] <= target.xMax and p[1] >= target.yMin and p[1] <= target.yMax):
            highestPoint = Utility.maxBy(positions, lambda p: p[1])[1]
            return (True, highestPoint)
    
    return (False, 0)

def findOptimalAngle(target: Target) -> int:
    maxXSpeed = target.xMax
    minXSpeed = 1 # suboptimal
    minYSpeed = target.yMin
    maxYSpeed = target.xMax # ? is there even an guaranteed optimal for all inputs?

    optimalHeight = 0
    optimalVector = (0, 0)

    for xV in range(minXSpeed, maxXSpeed):
        for yV in range(minYSpeed, maxYSpeed):
            hits, height = launchHitsTargetWithHighestPoint(target, xV, yV)
            if hits and height > optimalHeight:
                optimalVector = (xV, yV)
                optimalHeight = height

    return optimalVector, optimalHeight

def findValidAngleCount(target: Target) -> int:
    maxXSpeed = target.xMax
    minXSpeed = 1 # suboptimal
    minYSpeed = target.yMin
    maxYSpeed = -1 * target.yMin # due to arc y>0 being symmetrical

    validCount = 0
    for xV in range(minXSpeed, maxXSpeed + 1):
        for yV in range(minYSpeed, maxYSpeed + 1):
            hits, height = launchHitsTargetWithHighestPoint(target, xV, yV)
            if hits:
                print((xV, yV))
                validCount += 1

    return validCount
    

def solvePart1():
    target = Target()

    print('Solution to part1:')
    print(findOptimalAngle(target))


def solvePart2():
    target = Target()

    print('Solution to part2:')
    print(findValidAngleCount(target))


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
