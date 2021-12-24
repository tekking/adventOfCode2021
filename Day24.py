from typing import Iterator
import Utility
import cProfile
import timeit

filePath = 'input/day24/part1.txt'


def divideTowardsZero(a, b):
    if a * b >= 0:
        return a // b
    else:
        return -1 * (abs(a) // abs(b))


def convertLetterToIndex(letter):
    if letter == 'w':
        return 0
    if letter == 'x':
        return 1
    if letter == 'y':
        return 2
    if letter == 'z':
        return 3


def convertIndexToLetter(index):
    if index == 0:
        return 'w'
    if index == 1:
        return 'x'
    if index == 2:
        return 'y'
    if index == 3:
        return 'z'


# Note: Entire section on operations/alu simulation ended up unused in final method...
# region AluEngine
class Operation:
    def __init__(self) -> None:
        pass

    # returns new list of inputs, state is modified in place
    def execute(self, stateValues: list[int], inputs: list[int]):
        pass


class InpOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])

    def __repr__(self) -> str:
        return f'inp {convertIndexToLetter(self.targetIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        input = inputs.pop()
        stateValues[self.targetIndex] = input


class AddOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])
        if (arguments[1] < 'w'):
            self.constantOperation = True
            self.constantValue = int(arguments[1])
        else:
            self.constantOperation = False
            self.otherIndex = convertLetterToIndex(arguments[1])

    def __repr__(self) -> str:
        if self.constantOperation:
            return f'add {convertIndexToLetter(self.targetIndex)} {self.constantValue}'
        else:
            return f'add {convertIndexToLetter(self.targetIndex)} {convertIndexToLetter(self.otherIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        if self.constantOperation:
            stateValues[self.targetIndex] += self.constantValue
        else:
            stateValues[self.targetIndex] += stateValues[self.otherIndex]


class MulOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])
        if (arguments[1] < 'w'):
            self.constantOperation = True
            self.constantValue = int(arguments[1])
        else:
            self.constantOperation = False
            self.otherIndex = convertLetterToIndex(arguments[1])

    def __repr__(self) -> str:
        if self.constantOperation:
            return f'mul {convertIndexToLetter(self.targetIndex)} {self.constantValue}'
        else:
            return f'mul {convertIndexToLetter(self.targetIndex)} {convertIndexToLetter(self.otherIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        if self.constantOperation:
            stateValues[self.targetIndex] *= self.constantValue
        else:
            stateValues[self.targetIndex] *= stateValues[self.otherIndex]


class DivOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])
        if (arguments[1] < 'w'):
            self.constantOperation = True
            self.constantValue = int(arguments[1])
        else:
            self.constantOperation = False
            self.otherIndex = convertLetterToIndex(arguments[1])

    def __repr__(self) -> str:
        if self.constantOperation:
            return f'div {convertIndexToLetter(self.targetIndex)} {self.constantValue}'
        else:
            return f'div {convertIndexToLetter(self.targetIndex)} {convertIndexToLetter(self.otherIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        if self.constantOperation:
            stateValues[self.targetIndex] = divideTowardsZero(
                stateValues[self.targetIndex], self.constantValue)
        else:
            stateValues[self.targetIndex] = divideTowardsZero(
                stateValues[self.targetIndex], stateValues[self.otherIndex])


class ModOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])
        if (arguments[1] < 'w'):
            self.constantOperation = True
            self.constantValue = int(arguments[1])
        else:
            self.constantOperation = False
            self.otherIndex = convertLetterToIndex(arguments[1])

    def __repr__(self) -> str:
        if self.constantOperation:
            return f'mod {convertIndexToLetter(self.targetIndex)} {self.constantValue}'
        else:
            return f'mod {convertIndexToLetter(self.targetIndex)} {convertIndexToLetter(self.otherIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        if self.constantOperation:
            stateValues[self.targetIndex] %= self.constantValue
        else:
            stateValues[self.targetIndex] %= stateValues[self.otherIndex]


class EqlOperation:
    def __init__(self, arguments: list[str]) -> None:
        self.targetIndex = convertLetterToIndex(arguments[0])
        if (arguments[1] < 'w'):
            self.constantOperation = True
            self.constantValue = int(arguments[1])
        else:
            self.constantOperation = False
            self.otherIndex = convertLetterToIndex(arguments[1])

    def __repr__(self) -> str:
        if self.constantOperation:
            return f'eql {convertIndexToLetter(self.targetIndex)} {self.constantValue}'
        else:
            return f'eql {convertIndexToLetter(self.targetIndex)} {convertIndexToLetter(self.otherIndex)}'

    def execute(self, stateValues: list[int], inputs: list[int]):
        if self.constantOperation:
            stateValues[self.targetIndex] = 1 if stateValues[self.targetIndex] == self.constantValue else 0
        else:
            stateValues[self.targetIndex] = 1 if stateValues[self.targetIndex] == stateValues[self.otherIndex] else 0


def getInstructionFromLine(line: str) -> Operation:
    splitLine = line.split(' ')
    if len(splitLine) == 0:
        return None
    if splitLine[0] == 'inp':
        return InpOperation(splitLine[1:])
    if splitLine[0] == 'add':
        return AddOperation(splitLine[1:])
    if splitLine[0] == 'mul':
        return MulOperation(splitLine[1:])
    if splitLine[0] == 'div':
        return DivOperation(splitLine[1:])
    if splitLine[0] == 'mod':
        return ModOperation(splitLine[1:])
    if splitLine[0] == 'eql':
        return EqlOperation(splitLine[1:])


class Program:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)

        self.instructions = list(filter(lambda i: i != None,
                                        map(getInstructionFromLine, inputLines)))

    def initializeValues(self):
        self.values = [0 for i in range(4)]

    def executeProgram(self, inputs: list[int]) -> tuple[int, int, int, int]:
        self.initializeValues()
        for i in range(14):
            for j in range(18):
                if type(self.instructions[j]) != type(self.instructions[i * 18 + j]):
                    raise Exception('outside pattern')
                if type(self.instructions[j]) != InpOperation:
                    if self.instructions[j].constantOperation != self.instructions[i*18 + j].constantOperation:
                        raise Exception('outside pattern')
                    if not self.instructions[j].constantOperation:
                        if self.instructions[j].targetIndex != self.instructions[i*18 + j].targetIndex:
                            raise Exception('outside pattern')

        for index, ins in enumerate(self.instructions):
            ins.execute(self.values, inputs)
        return self.values
# endregion AluEngine


class HandDecodedProgram:
    def __init__(self) -> None:
        self.constant1 = (1, 1, 1, 26, 1, 1, 26, 1, 26, 1, 26, 26, 26, 26)
        self.constant2 = (15, 14, 11, -13, 14, 15, -7,
                          10, -12, 15, -16, -9, -8, -8)
        self.constant3 = (4, 16, 14, 3, 11, 13, 11, 7, 12, 15, 13, 1, 15, 4)

    def calculateInput(self, input: list[int]) -> int:
        result = 0
        for i, inputI in enumerate(input):
            if (result % 26) + self.constant2[i] == inputI:
                result = (divideTowardsZero(
                    result, self.constant1[i]) * 26 + inputI + self.constant3[i])
            else:
                result = divideTowardsZero(result, self.constant1[i])

    def runStep(self, z, indexOfStep, inputForStep) -> int:
        if (z % 26) + self.constant2[indexOfStep] != inputForStep:
            return (divideTowardsZero(z, self.constant1[indexOfStep]) * 26 + inputForStep + self.constant3[indexOfStep])
        else:
            return divideTowardsZero(z, self.constant1[indexOfStep])


def modelNumberGenerator(range, length: int) -> Iterator[list[int]]:
    if length == 1:
        for i in range:
            yield [i]
    else:
        for r in modelNumberGenerator(range, length - 1):
            for i in range:
                yield r + [i]


def solvePart1():
    handProgram = HandDecodedProgram()
    digitRange = [i for i in range(9, 0, -1)]

    # Thresholds based on the fact that z shrinks at most by factor Ci1 per step (which is 1 or 26)
    possibleThresholds = (26 ** 7,
                          26 ** 7,
                          26 ** 7,
                          26 ** 7,
                          26 ** 6,
                          26 ** 6,
                          26 ** 6,
                          26 ** 5,
                          26 ** 5,
                          26 ** 4,
                          26 ** 4,
                          26 ** 3,
                          26 ** 2,
                          26)

    # Find state for prefix after n steps (since only relevant state between steps is z)
    prefixes = [([], 0)]
    for n in range(14):
        print(n)
        print(len(prefixes))
        newPrefixes = []
        encounteredValues = set()
        possibleThreshold = possibleThresholds[n]
        for prefix in prefixes:
            if (prefix[1] > possibleThreshold):
                continue

            for nextDigit in digitRange:
                result = handProgram.runStep(prefix[1], n, nextDigit)
                if not result in encounteredValues:
                    encounteredValues.add(result)
                    newPrefixes.append((prefix[0] + [nextDigit], result))
        prefixes = newPrefixes

    print('Solution to part1:')
    zeroPrefixes = list(filter(lambda p: p[1] == 0, prefixes))
    print(zeroPrefixes)
    print()


def solvePart2():
    handProgram = HandDecodedProgram()
    digitRange = [i for i in range(1, 10)]

    # Thresholds based on the fact that z shrinks at most by factor Ci1 per step (which is 1 or 26)
    possibleThresholds = (26 ** 7,
                          26 ** 7,
                          26 ** 7,
                          26 ** 7,
                          26 ** 6,
                          26 ** 6,
                          26 ** 6,
                          26 ** 5,
                          26 ** 5,
                          26 ** 4,
                          26 ** 4,
                          26 ** 3,
                          26 ** 2,
                          26)

    # Find state for prefix after n steps (since only relevant state between steps is z)
    prefixes = [([], 0)]
    for n in range(14):
        print(n)
        print(len(prefixes))
        newPrefixes = []
        encounteredValues = set()
        possibleThreshold = possibleThresholds[n]
        for prefix in prefixes:
            if (prefix[1] > possibleThreshold):
                continue

            for nextDigit in digitRange:
                result = handProgram.runStep(prefix[1], n, nextDigit)
                if not result in encounteredValues:
                    encounteredValues.add(result)
                    newPrefixes.append((prefix[0] + [nextDigit], result))
        prefixes = newPrefixes

    print('Solution to part2:')
    zeroPrefixes = list(filter(lambda p: p[1] == 0, prefixes))
    print(zeroPrefixes)
    print()


if(__name__ == '__main__'):
    # cProfile.run('solvePart1()')
    # result = timeit.timeit('solvePart1()', setup='gc.enable(); from __main__ import solvePart1', number=1)
    # print(result)
    solvePart1()
    solvePart2()
