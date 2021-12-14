import Utility

filePath = 'input/day09/part1.txt'


class HeightMap:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)
        self.heights = []
        for line in inputLines:
            heightsInLine = list(map(int, line))
            self.heights.append(heightsInLine)

    def height(self):
        return len(self.heights)

    def width(self):
        return len(self.heights[0])

    def getAdjacentPoints(self, y, x) -> list[tuple[int, int]]:
        results = []
        if(y > 0):
            results.append((y - 1, x))
        if(x > 0):
            results.append((y, x - 1))
        if(y < self.height() - 1):
            results.append((y + 1, x))
        if(x < self.width() - 1):
            results.append((y, x + 1))
        return results

    def findLowPointCoordinates(self) -> list[tuple[int, int]]:
        lowPoints = []

        for y in range(self.height()):
            for x in range(self.width()):
                isLowPoint = True
                pointHeight = self.heights[y][x]
                adjacentTiles = self.getAdjacentPoints(y, x)
                for tileY, tileX in adjacentTiles:
                    if (self.heights[tileY][tileX] <= pointHeight):
                        isLowPoint = False
                        break
                if(isLowPoint):
                    lowPoints.append((y, x))

        return lowPoints

    def findLowPointHeights(self) -> list[int]:
        lowPoints = self.findLowPointCoordinates()

        return list(map(lambda c: self.heights[c[0]][c[1]], lowPoints))

    def findBasinSizes(self) -> list[int]:
        lowPoints = self.findLowPointCoordinates()
        basins = list(map(lambda x: [x], lowPoints))

        for basin in basins:
            newElements = basin.copy()
            while(len(newElements) > 0):
                e = newElements.pop()
                eHeight = self.heights[e[0]][e[1]]
                neighbors = self.getAdjacentPoints(e[0], e[1])
                for neighbor in neighbors:
                    existingInBasin = next((x for x in basin if x[0] == neighbor[0] and x[1] == neighbor[1]), None)
                    if(existingInBasin != None):
                        continue
                    neighborHeight = self.heights[neighbor[0]][neighbor[1]]
                    if(neighborHeight < 9 and neighborHeight > eHeight):
                        basin.append(neighbor)
                        newElements.append(neighbor)

        return list(map(len, basins))


def solvePart1():
    hMap = HeightMap()
    lowPointHeights = hMap.findLowPointHeights()
    risks = sum(map(lambda h: h + 1, lowPointHeights))

    print('Solution to part1:')
    print(lowPointHeights)
    print(risks)


def solvePart2():
    hMap = HeightMap()
    basinSizes = hMap.findBasinSizes()
    orderedSizes = sorted(basinSizes, reverse=True)

    print('Solution to part2:')
    print(orderedSizes[0] * orderedSizes[1] * orderedSizes[2])


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
