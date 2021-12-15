import Utility

filePath = 'input/day11/part1.txt'


class OctopusSwarm:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)
        self.octopuses = [[0 for i in range(10)] for i in range(10)]
        self.totalFlashes = 0
        for i, line in enumerate(inputLines):
            for j, c in enumerate(line):
                self.octopuses[i][j] = int(c)

    def stepN(self, n):
        for i in range(n):
            self.step()

    def findFullFlashStep(self):
        for i in range(1, 10000000):
            if(self.step()):
                return i


    def step(self):
        flashesThisStep = 0
        flashing = []
        for y in range(10):
            for x in range(10):
                self.octopuses[y][x] += 1
                if(self.octopuses[y][x] == 10):
                    flashing.append((y, x))

        while(len(flashing) > 0):
            self.totalFlashes += 1
            flashesThisStep += 1
            fY, fX = flashing.pop()
            neighbors = self.getNeighbors(fY, fX)
            for nY, nX in neighbors:
                self.octopuses[nY][nX] += 1
                if (self.octopuses[nY][nX] == 10):
                    flashing.append((nY, nX))

        for y in range(10):
            for x in range(10):
                if(self.octopuses[y][x] > 9):
                    self.octopuses[y][x] = 0

        return flashesThisStep == 100

    def getNeighbors(self, y, x):
        possibleNeighbors = []
        for xd in range(-1, 2):
            for yd in range(-1, 2):
                if(xd == 0 and yd == 0):
                    continue
                possibleNeighbors.append((y + yd, x + xd))

        return list(filter(lambda c: c[1] >= 0 and c[1] < 10 and c[0] >= 0 and c[0] < 10, possibleNeighbors))


def solvePart1():
    swarm = OctopusSwarm()
    swarm.stepN(100)

    print('Solution to part1:')
    print(swarm.totalFlashes)


def solvePart2():
    swarm = OctopusSwarm()
    fullFlashStep = swarm.findFullFlashStep()

    print('Solution to part2:')
    print(fullFlashStep)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
