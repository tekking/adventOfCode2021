import Utility

filePath = 'input/day05/part1.txt'


class Line:
    def __init__(self, inputLine) -> None:
        start, end = inputLine.split(' -> ')
        self.startX = int(start.split(',')[1])
        self.startY = int(start.split(',')[0])
        self.endX = int(end.split(',')[1])
        self.endY = int(end.split(',')[0])

    def isHorizontal(self) -> bool:
        return self.startY == self.endY

    def isVertical(self) -> bool:
        return self.startX == self.endX

    def isDiagonal(self) -> bool:
        return not (self.isHorizontal() or self.isVertical())

    def __repr__(self) -> str:
        return self.startX + ',' + self.startY + ' -> ' + self.endX + ',' + self.endY


class Field:
    size = 1000

    def __init__(self) -> None:
        self.heights = [[0 for i in range(Field.size)]
                        for i in range(Field.size)]

    def loadHorizontalAndVerticalLines(self, lines: list[Line]):
        for line in lines:
            if (not (line.isHorizontal() or line.isVertical())):
                continue
            self.loadLine(line)

    def loadLines(self, lines: list[Line]):
        for line in lines:
            self.loadLine(line)

    def loadLine(self, line: Line):
        lengthOfLine = max(abs(line.endY - line.startY), abs(line.endX - line.startX))
        xChange = (line.endX - line.startX) // lengthOfLine
        yChange = (line.endY - line.startY) // lengthOfLine
        for i in range(lengthOfLine + 1):
            x = line.startX + i * xChange
            y = line.startY + i * yChange
            self.heights[x][y] += 1

    def getOverlapPointsCount(self) -> int:
        sum = 0
        for x in range(Field.size):
            for y in range(Field.size):
                if (self.heights[x][y] > 1):
                    sum += 1
        return sum


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    lines = list(map(Line, inputLines))
    field = Field()
    field.loadHorizontalAndVerticalLines(lines)

    print('Solution to part1:')
    print(field.getOverlapPointsCount())


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    lines = list(map(Line, inputLines))
    field = Field()
    field.loadLines(lines)

    print('Solution to part2:')
    print(field.getOverlapPointsCount())


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
