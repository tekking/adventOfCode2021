import Utility

filePath = 'input/day10/part1.txt'


def findFirstIllegalCharInLine(line):
    chunkStack = []
    for newChar in line:
        if (newChar == '(' or newChar == '<' or newChar == '[' or newChar == '{'):
            chunkStack.append(newChar)
        else:
            currentChunk = chunkStack.pop()
            if(abs(ord(newChar) - ord(currentChunk)) > 2):
                return newChar
    return ''


def findLegalLines(inputLines):
    legalLines = []
    for line in inputLines:
        if(findFirstIllegalCharInLine(line) == ''):
            legalLines.append(line)
    return legalLines


def getUnfinishedStackForLegalLine(line):
    chunkStack = []
    for newChar in line:
        if (newChar == '(' or newChar == '<' or newChar == '[' or newChar == '{'):
            chunkStack.append(newChar)
        else:
            currentChunk = chunkStack.pop()
            if(abs(ord(newChar) - ord(currentChunk)) > 2):
                raise BaseException('Should not happen!!!!')
    return chunkStack


def scoreUnfinishedLine(line):
    remainingStack = getUnfinishedStackForLegalLine(line)
    score = 0
    while(len(remainingStack) > 0):
        nextChar = remainingStack.pop()
        score *= 5
        if(nextChar == '('):
            score += 1
        if(nextChar == '['):
            score += 2
        if(nextChar == '{'):
            score += 3
        if(nextChar == '<'):
            score += 4
    return score


def findAllIllegalChars(inputLines):
    results = []
    for line in inputLines:
        illegal = findFirstIllegalCharInLine(line)
        if (illegal != ''):
            results.append(illegal)
    return results


def findTotalIllegalScore(inputLines):
    illegalChars = findAllIllegalChars(inputLines)
    totalScore = 0
    for c in illegalChars:
        if(c == ')'):
            totalScore += 3
        if(c == ']'):
            totalScore += 57
        if(c == '}'):
            totalScore += 1197
        if(c == '>'):
            totalScore += 25137
    return totalScore


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    score = findTotalIllegalScore(inputLines)

    print('Solution to part1:')
    print(score)


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    legalLines = findLegalLines(inputLines)
    scoresForLegalLines = list(map(scoreUnfinishedLine, legalLines))
    sortedScores = sorted(scoresForLegalLines)
    median = sortedScores[len(sortedScores) // 2]

    print('Solution to part2:')
    print(median)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
