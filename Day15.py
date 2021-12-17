import Utility
from collections import deque
import time
import cProfile

filePath = 'input/day15/part1.txt'


class Cave:
    def __init__(self) -> None:
        pass

    def initializeNormal(self):
        self.initializeExpanded()

    def initializeExpanded(self, repeats = 1):
        inputLines = Utility.getLinesFromFile(filePath)
        self.layout = []
        for i in range(repeats):
            for l in inputLines:
                row = []
                for j in range(repeats):
                    for c in l:
                        rawValue = int(c)
                        realValue = ((rawValue + i + j - 1) % 9) + 1
                        row.append(realValue)
                self.layout.append(row)

        self.height = len(self.layout)
        self.width = len(self.layout[0])
        self.setupNeighborLookup()

    def setupNeighborLookup(self):
        self.neighborLookup = [[[] for i in range(self.width)] for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.neighborLookup[y][x] = self.getNeighbors(y, x)

    def getNeighbors(self, y, x):
        results = []
        if(y > 0):
            results.append((y - 1, x))
        if(x > 0):
            results.append((y, x - 1))
        if(y < self.height - 1):
            results.append((y + 1, x))
        if(x < self.width - 1):
            results.append((y, x + 1))
        return results

    # better :)
    def findShortestPathLengthQueue(self):
        height = self.height
        width = self.width
        pathLengthMap = [
            [width*height*9 for i in range(width)] for i in range(height)]
        pathLengthMap[height - 1][width - 1] = 0
        queue = deque([(height-1, width-1)])
        while(len(queue) > 0):
            ey, ex = queue.popleft()
            elementCost = self.layout[ey][ex]
            elementPathCost = pathLengthMap[ey][ex]
            sumCost = elementCost + elementPathCost
            neighbors = self.neighborLookup[ey][ex]
            for ny, nx in neighbors:
                if sumCost < pathLengthMap[ny][nx]:
                    pathLengthMap[ny][nx] = sumCost
                    queue.append((ny, nx))

        # with open("lengthmap.txt", 'w+') as file:
        #     for row in pathLengthMap:
        #         file.write(''.join(['\t' + str(i) for i in row]))
        #         file.write('\n')

        # with open("heightmmap.txt", 'w+') as file:
        #     for row in self.layout:
        #         file.write(''.join(['\t' + str(i) for i in row]))
        #         file.write('\n')
        return pathLengthMap[0][0]


    def findShortestPathLength(self):
        height = self.height
        width = self.width
        pathLengthMap = [
            [width*height*9 for i in range(width)] for i in range(height)]
        pathLengthMap[height - 1][width - 1] = 0
        stack = {(height-1, width-1)}
        while(len(stack) > 0):
            ey, ex = stack.pop()
            elementCost = self.layout[ey][ex]
            elementPathCost = pathLengthMap[ey][ex]
            sumCost = elementCost + elementPathCost
            neighbors = self.getNeighbors(ey, ex)
            for ny, nx in neighbors:
                if sumCost < pathLengthMap[ny][nx]:
                    pathLengthMap[ny][nx] = sumCost
                    stack.add((ny, nx))

        # with open("lengthmap.txt", 'w+') as file:
        #     for row in pathLengthMap:
        #         file.write(''.join(['\t' + str(i) for i in row]))
        #         file.write('\n')

        # with open("heightmmap.txt", 'w+') as file:
        #     for row in self.layout:
        #         file.write(''.join(['\t' + str(i) for i in row]))
        #         file.write('\n')
        return pathLengthMap[0][0]


def solvePart1():
    cave = Cave()
    cave.initializeNormal()

    t = time.process_time()
    shortestPathLength = cave.findShortestPathLengthQueue()
    print(time.process_time() - t)

    print('Solution to part1:')
    print(shortestPathLength)


def solvePart2():
    cave = Cave()
    cave.initializeExpanded(5)

    t = time.process_time()
    shortestPathLength = cave.findShortestPathLengthQueue()
    print(time.process_time() - t)

    print('Solution to part2:')
    print(shortestPathLength)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()

    # cProfile.run('solvePart1()')
    # cProfile.run('solvePart2()')
