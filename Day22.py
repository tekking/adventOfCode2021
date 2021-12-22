from __future__ import annotations
import Utility

filePath = 'input/day22/part1.txt'


class DumbCube:
    def __init__(self) -> None:
        self.cubes = {}

    def getCubeOn(self, x, y, z) -> bool:
        return self.cubes.get((x, y, z), False)

    def getOnCountWithinCore(self) -> int:
        onCount = 0
        for x in range(-50, 51):
            for y in range(-50, 51):
                for z in range(-50, 51):
                    if self.getCubeOn(x, y, z):
                        onCount += 1
        return onCount

    def executeInstruction(self, instructionLine: str):
        on = instructionLine.split(' ')[0] == 'on'
        rangePart = instructionLine.split(' ')[1]
        xPart, yPart, zPart = rangePart.split(',')
        xStart, xEnd = list(map(int, xPart.split('=')[1].split('..')))
        yStart, yEnd = list(map(int, yPart.split('=')[1].split('..')))
        zStart, zEnd = list(map(int, zPart.split('=')[1].split('..')))

        for x in range(Utility.maxBy([-50, xStart]), Utility.minBy([51, xEnd + 1])):
            for y in range(Utility.maxBy([-50, yStart]), Utility.minBy([51, yEnd + 1])):
                for z in range(Utility.maxBy([-50, zStart]), Utility.minBy([51, zEnd + 1])):
                    self.cubes.update({(x, y, z): on})


class CubeSection:
    def __init__(self, xStart, xEnd, yStart, yEnd, zStart, zEnd) -> None:
        self.xStart = xStart
        self.xEnd = xEnd
        self.yStart = yStart
        self.yEnd = yEnd
        self.zStart = zStart
        self.zEnd = zEnd

    def getIntersection(self, otherSection: CubeSection) -> CubeSection or None:
        if ((otherSection.xStart > self.xEnd or otherSection.xEnd < self.xStart) or
            (otherSection.yStart > self.yEnd or otherSection.yEnd < self.yStart) or
                (otherSection.zStart > self.zEnd or otherSection.zEnd < self.zStart)):
            return None

        xStart = Utility.maxBy([otherSection.xStart, self.xStart])
        xEnd = Utility.minBy([otherSection.xEnd, self.xEnd])
        yStart = Utility.maxBy([otherSection.yStart, self.yStart])
        yEnd = Utility.minBy([otherSection.yEnd, self.yEnd])
        zStart = Utility.maxBy([otherSection.zStart, self.zStart])
        zEnd = Utility.minBy([otherSection.zEnd, self.zEnd])

        return CubeSection(xStart, xEnd, yStart, yEnd, zStart, zEnd)

    def getVolume(self) -> int:
        # Naive for speed, assumes end >= start on all axis
        return (self.xEnd - self.xStart + 1) * (self.yEnd - self.yStart + 1) * (self.zEnd - self.zStart + 1)

    def __repr__(self) -> str:
        return f'x={self.xStart}..{self.xEnd}, y={self.yStart}..{self.yEnd}, z={self.zStart}..{self.yEnd}'


class SmartCube:
    def __init__(self) -> None:
        self.onCount = 0
        self.onSections: list[CubeSection] = []
        self.offSections: list[CubeSection] = []

    def executeInstruction(self, instructionLine: str):
        on = instructionLine.split(' ')[0] == 'on'
        rangePart = instructionLine.split(' ')[1]
        xPart, yPart, zPart = rangePart.split(',')
        xStart, xEnd = list(map(int, xPart.split('=')[1].split('..')))
        yStart, yEnd = list(map(int, yPart.split('=')[1].split('..')))
        zStart, zEnd = list(map(int, zPart.split('=')[1].split('..')))
        newCubeSection = CubeSection(xStart, xEnd, yStart, yEnd, zStart, zEnd)
        self.executeCubeSection(on, newCubeSection)

    def executeCubeSection(self, on, cubeSection: CubeSection):
        # Functions by inclusion/exclusion principle, building inclusion/exclusion sets
        # as lines are processed, which help determine the correct total change to onCount
        # on processing any line.
        newOnSections = []
        newOffSections = []
        if on:
            self.onCount += cubeSection.getVolume()
            newOnSections.append(cubeSection)

        for s in self.onSections:
            interSection = s.getIntersection(cubeSection)
            if(interSection == None):
                continue
            self.onCount -= interSection.getVolume()
            newOffSections.append(interSection)

        for s in self.offSections:
            interSection = s.getIntersection(cubeSection)
            if(interSection == None):
                continue
            self.onCount += interSection.getVolume()
            newOnSections.append(interSection)

        self.onSections.extend(newOnSections)
        self.offSections.extend(newOffSections)


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)

    cube = DumbCube()
    for l in inputLines:
        cube.executeInstruction(l)

    print('Solution to part1:')
    print(cube.getOnCountWithinCore())


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    cube = SmartCube()
    for l in inputLines:
        cube.executeInstruction(l)

    print('Solution to part2:')
    print(cube.onCount)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
