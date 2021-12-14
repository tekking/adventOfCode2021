import Utility

filePath = 'input/day08/part1.txt'


def getChannels(letters: str) -> list[int]:
    channels = [0 for i in range(7)]
    for c in letters:
        channels[ord(c) - 97] += 1
    return channels


def parseLine(line: str) -> tuple[list[list[int]], list[list[int]]]:
    examplePart, outputPart = line.split(' | ')
    exampleStrings = examplePart.split(' ')
    outputStrings = outputPart.split(' ')

    examples = list(map(getChannels, exampleStrings))
    outputs = list(map(getChannels, outputStrings))

    return examples, outputs

""" 0: 6
    1: 2
    2: 5
    3: 5
    4: 4
    5: 5
    6: 6
    7: 3
    8: 7
    9: 6
"""

def overlap(leftChannels, rightChannels): 
    return [leftChannels[i] and rightChannels[i] for i in range(len(leftChannels))]

def equal(leftChannels, rightChannels):
    return sum(overlap(leftChannels, rightChannels)) == sum(leftChannels) and sum(leftChannels) == sum(rightChannels)

def solveLine(line: str) -> int:
    examples, outputs = parseLine(line)
    lookup = [[] for i in range(10)]
    lookup[1] = next(x for x in examples if sum(x) == 2)
    lookup[4] = next(x for x in examples if sum(x) == 4)
    lookup[7] = next(x for x in examples if sum(x) == 3)
    lookup[8] = next(x for x in examples if sum(x) == 7)
    lookup[9] = next(x for x in examples if sum(x) == 6 and sum(overlap(x, lookup[4])) == 4)
    lookup[0] = next(x for x in examples if sum(x) == 6 and (not equal(x, lookup[9])) and sum(overlap(x, lookup[1])) == 2)
    lookup[6] = next(x for x in examples if sum(x) == 6 and (not equal(x, lookup[9])) and sum(overlap(x, lookup[1])) == 1)
    lookup[3] = next(x for x in examples if sum(x) == 5 and sum(overlap(x, lookup[1])) == 2)
    lookup[5] = next(x for x in examples if sum(x) == 5 and (not equal(x, lookup[3])) and sum(overlap(x, lookup[4])) == 3)
    lookup[2] = next(x for x in examples if sum(x) == 5 and (not equal(x, lookup[3])) and (not equal(x, lookup[5])))
    
    digits = []
    for o in outputs:
        for i in range(10):
            if(equal(o, lookup[i])):
                digits.append(i)
                continue

    value = digits[0] * 1000 + digits[1] * 100 + digits[2] * 10 + digits[3]
    return value

def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    total = 0
    for line in inputLines:
        examples, outputs = parseLine(line)
        for output in outputs:
            if (sum(output) == 2
                    or sum(output) == 4
                    or sum(output) == 3
                    or sum(output) == 7):
                total += 1

    print('Solution to part1:')
    print(total)


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    outputs = []
    for line in inputLines:
        outputs.append(solveLine(line))

    print('Solution to part2:')
    print(sum(outputs))

if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
