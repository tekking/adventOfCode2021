from __future__ import annotations
from os import path
import Utility

filePath = 'input/day12/part1.txt'


def isLargeCave(location):
    for c in location:
        if (ord(c) > 90):
            return False
    return True


class Map:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)
        self.locations = set()
        self.paths = {}
        for line in inputLines:
            left, right = line.split('-')
            self.locations.add(left)
            self.locations.add(right)
            if(self.paths.get(left) == None):
                self.paths.update({left: []})
            self.paths[left].append(right)
            if(self.paths.get(right) == None):
                self.paths.update({right: []})
            self.paths[right].append(left)

    def getDirectionsFromLocation(self, location):
        return self.paths[location]


class Path:
    def __init__(self, visited = {'start'}, location = 'start', history = ['start'], canVisitSmallTwice = False) -> None:
        self.visited = visited  # Set of visited (small) caves
        self.location = location  # Current location
        self.history = history  # History of locations
        self.canVisitSmallTwice = canVisitSmallTwice # can still visit a small cave twice

    def iterate(self, map: Map) -> list[Path]:
        newPaths = []
        possibleDirections = map.getDirectionsFromLocation(self.location)
        if(self.canVisitSmallTwice):
            validDirections = list(filter(lambda d: d != 'start', possibleDirections))
        else:
            validDirections = list(
                filter(
                    lambda d: isLargeCave(d) or
                    (not d in self.visited), possibleDirections))

        for direction in validDirections:
            newSet = self.visited.copy()
            newSet.add(direction)
            newHistory = self.history.copy()
            newHistory.append(direction)
            if(direction in self.visited and (not isLargeCave(direction))):
                newPaths.append(Path(newSet, direction, newHistory, False))
            else:
                newPaths.append(Path(newSet, direction, newHistory, self.canVisitSmallTwice))
        return newPaths

    def isFinished(self):
        return self.location == 'end'

    def visitsSmallCave(self):
        for l in self.history:
            if(not isLargeCave(l) and l != 'start' and l != 'end'):
                return True
        return False

    def __repr__(self) -> str:
        repr = self.history[0]
        for l in self.history[1:]:
            repr += ',' + l
        return repr

def findAllPathsForMap(map, smallTwice = False):
    initialPath = Path(canVisitSmallTwice=smallTwice)
    paths = [initialPath]
    finishedPaths = []
    while(len(paths) > 0):
        path = paths.pop()
        newPaths = path.iterate(map)
        for np in newPaths:
            if(np.isFinished()):
                finishedPaths.append(np)
            else:
                paths.append(np)
    
    return finishedPaths

def solvePart1():
    map = Map()
    paths = findAllPathsForMap(map)
    smallCavePaths = list(filter(lambda p: p.visitsSmallCave(), paths))

    print('Solution to part1:')
    print(len(smallCavePaths))


def solvePart2():
    map = Map()
    paths = findAllPathsForMap(map, True)

    print('Solution to part2:')
    print(len(paths))


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
