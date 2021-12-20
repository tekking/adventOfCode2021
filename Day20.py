import Utility

filePath = 'input/day20/part1.txt'


def getTransformLookup() -> dict[int, bool]:
    inputLines = Utility.getLinesFromFile(filePath)
    line = inputLines[0]
    result = {}
    for i in range(len(line)):
        result.update({i: line[i] == '#'})
    return result


class Image:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)
        imageLines = inputLines[2:]
        self.imageLookup = {}
        for i, l in enumerate(imageLines):
            for j, c in enumerate(l):
                self.imageLookup.update({(j, i): c == '#'})

        self.minY = 0
        self.minX = 0
        self.maxY = len(imageLines)
        self.maxX = len(imageLines[0])
        self.currentBackground = False
        self.transformLookup = getTransformLookup()

    def getPixel(self, x: int, y: int) -> bool:
        if (x < self.minX or x >= self.maxX or y < self.minY or y >= self.maxY):
            return self.currentBackground

        return self.imageLookup[(x, y)]

    def iterate(self):
        newImageLookup = {}
        for x in range(self.minX - 1, self.maxX + 1):
            for y in range(self.minY - 1, self.maxY + 1):
                newImageLookup.update({(x, y): self.determineNewPixel(x, y)})
        self.imageLookup = newImageLookup

        self.minX -= 1
        self.maxX += 1
        self.minY -= 1
        self.maxY += 1

        if self.currentBackground:
            self.currentBackground = self.transformLookup[511]
        else:
            self.currentBackground = self.transformLookup[0]

    def determineNewPixel(self, x, y) -> bool:
        bitBuildup = []
        for yDelta in range(-1, 2):
            for xDelta in range(-1, 2):
                bitBuildup.append('1' if self.getPixel(
                    x + xDelta, y + yDelta) else '0')
        bitString = ''.join(bitBuildup)
        value = int(bitString, 2)
        return self.transformLookup[value]

    def __repr__(self) -> str:
        outputBuildup = []
        for y in range(self.minY - 1, self.maxY + 1):
            lineBuildup = []
            for x in range(self.minX - 1, self.maxX + 1):
                lineBuildup.append('#' if self.getPixel(x, y) else '.')
            outputBuildup.append(''.join(lineBuildup))
            outputBuildup.append('\n')
        return ''.join(outputBuildup)

    def getLitCount(self) -> int:
        if(self.currentBackground):
            raise Exception('infinite lit pixels')
        
        count = 0
        for x in range(self.minX, self.maxX):
            for y in range(self.minY, self.maxY):
                if self.imageLookup[(x, y)]:
                    count += 1
        return count

    def iterateNTimes(self, n):
        for i in range(n):
            self.iterate()


def solvePart1():
    image = Image()
    print(image)
    image.iterate()
    print(image)
    image.iterate()
    print(image)

    print('Solution to part1:')
    print(image.getLitCount())


def solvePart2():
    image = Image()
    image.iterateNTimes(50)

    print('Solution to part2:')
    print(image.getLitCount())


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
