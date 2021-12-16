import Utility

filePath = 'input/day13/part1.txt'


class Fold:
    def __init__(self, line) -> None:
        relevantPart = line.split(' ')[2]
        direction, index = relevantPart.split('=')
        self.alongX = direction == 'x'
        self.index = int(index)

    def foldPointSet(self, pointSet):
        newPointSet = set()
        if self.alongX:
            for px, py in pointSet:
                if px < self.index:
                    newPointSet.add((px, py))
                else:
                    newX = self.index - (px - self.index)
                    newPointSet.add((newX, py))
        else:
            for px, py in pointSet:
                if py < self.index:
                    newPointSet.add((px, py))
                else:
                    newY = self.index - (py - self.index)
                    newPointSet.add((px, newY))
        return newPointSet


def getStartPointSet():
    inputLines = Utility.getLinesFromFile(filePath)
    pointSet = set()
    for l in inputLines:
        if (l == ''):
            break
        x, y = list(map(int, l.split(',')))
        pointSet.add((x, y))
    return pointSet


def getFolds() -> list[Fold]:
    inputLines = Utility.getLinesFromFile(filePath)
    folds = []
    for l in inputLines:
        if (not l.startswith('fold along')):
            continue
        folds.append(Fold(l))
    return folds

def renderPointSet(pointSet):
    maxX = Utility.maxBy(map(lambda p: p[0], pointSet))
    maxY = Utility.maxBy(map(lambda p: p[1], pointSet))
    roster = [[' ' for i in range(maxX + 1)] for i in range(maxY + 1)]
    for p in pointSet:
        roster[p[1]][p[0]] = 'X'
    for row in roster:
        print(row)

def solvePart1():
    pointSet = getStartPointSet()
    folds = getFolds()

    for f in folds:
        pointSet = f.foldPointSet(pointSet)
        print(len(pointSet))

    print('Solution to part1:')
    print(pointSet)
    print(len(pointSet))


def solvePart2():
    pointSet = getStartPointSet()
    folds = getFolds()

    for f in folds:
        pointSet = f.foldPointSet(pointSet)

    print('Solution to part2:')
    renderPointSet(pointSet)

if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
