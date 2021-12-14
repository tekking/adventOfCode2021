import Utility

filePath = 'input/day06/part1.txt'


def getInitialPopulationSpread(inputLines: list[str]) -> list[int]:
    members =  list(map(int, inputLines[0].split(',')))
    populationSpread = []
    for i in range(9):
        populationSpread.append(len(list(filter(lambda m: m == i, members))))

    return populationSpread


def stepPopulation(populationSpread: list[int]) -> list[int]:
    newSpread = [0 for i in range(9)]
    for i in range(8):
        newSpread[i] += populationSpread[i + 1]

    newSpread[8] += populationSpread[0]
    newSpread[6] += populationSpread[0]

    return newSpread


def simulatePopulation(populationSpread, steps):
    for i in range(steps):
        populationSpread = stepPopulation(populationSpread)
    return populationSpread


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    population = getInitialPopulationSpread(inputLines)

    print('Solution to part1:')
    print(sum(simulatePopulation(population, 80)))


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    population = getInitialPopulationSpread(inputLines)

    print('Solution to part2:')
    print(sum(simulatePopulation(population, 256)))


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
