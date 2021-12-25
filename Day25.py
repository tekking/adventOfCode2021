import Utility

filePath = 'input/day25/part1.txt'

class Ocean:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)
        self.eastFacing = set()
        self.southFacing = set()
        self.width = len(inputLines[0])
        self.heigth = len(inputLines)
        for y, line in enumerate(inputLines):
            for x, c in enumerate(line):
                if c == '>':
                    self.eastFacing.add((x, y))
                elif c == 'v':
                    self.southFacing.add((x, y))

    def iterate(self) -> bool:
        movement = False
        newEastFacing = set()
        for (x, y) in self.eastFacing:
            newPosition = ((x + 1) % self.width, y)

            if (not newPosition in self.eastFacing and not newPosition in self.southFacing):
                newEastFacing.add(newPosition)
                movement = True
            else:
                newEastFacing.add((x, y))

        self.eastFacing = newEastFacing
        
        newSouthFacing = set()
        for (x, y) in self.southFacing:
            newPosition = (x, (y + 1) % self.heigth)

            if (not newPosition in self.eastFacing and not newPosition in self.southFacing):
                newSouthFacing.add(newPosition)
                movement = True
            else:
                newSouthFacing.add((x, y))

        self.southFacing = newSouthFacing
        return movement

    def iterateUntilStopped(self) -> int:
        iteration = 1
        while(True):
            print(iteration)
            moved = self.iterate()
            if not moved:
                return iteration
            iteration += 1

    def printToConsole(self):
        for y in range(0, self.heigth):
            line = ''
            for x in range(0, self.width):
                if (x, y) in self.eastFacing:
                    line += '>'
                elif (x, y) in self.southFacing:
                    line += 'v'
                else:
                    line += '.'
            print(line)


def solvePart1():
    ocean = Ocean()
    final = ocean.iterateUntilStopped()

    print('Solution to part1:')
    print(final)


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    
    print('Solution to part2:')


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
