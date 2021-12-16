import Utility

filePath = 'input/day14/part1.txt'


def increasePairCount(pairCount, pair, amount=1):
    existingValue = pairCount.get(pair, 0)
    pairCount.update({pair: existingValue + amount})


class Rules:
    def __init__(self) -> None:
        inputLines = Utility.getLinesFromFile(filePath)

        self.rules = {}
        for l in inputLines[2:]:
            pair, output = l.split(' -> ')
            l, r = pair
            self.rules.update({(l, r): output})

    def applyRules(self, polymer):
        result = []
        for i in range(len(polymer) - 1):
            pair = (polymer[i], polymer[i + 1])
            ruleOutput = self.rules.get(pair)
            result.append(pair[0])
            if(ruleOutput != None):
                result.append(ruleOutput)
        result.append(polymer[len(polymer) - 1])
        return ''.join(result)

    def applyRulesToPairCount(self, pairCount):
        newPairCount = {}
        for pair, count in pairCount.items():
            ruleOutput = self.rules.get(pair)
            if ruleOutput == None:
                increasePairCount(newPairCount, pair, count)
            else:
                increasePairCount(newPairCount, (pair[0], ruleOutput), count)
                increasePairCount(newPairCount, (ruleOutput, pair[1]), count)
        return newPairCount

    def createNStepLookup(self, stepSize) -> dict[tuple[str, str], str]:
        letterSet = set()
        lookup = {}
        for rule in self.rules.items():
            letterSet.add(rule[0][0])
            letterSet.add(rule[0][1])
        for left in letterSet:
            for right in letterSet:
                polymer = left + right
                for i in range(stepSize):
                    polymer = self.applyRules(polymer)
                lookup.update({(left, right): polymer})
        return lookup

    def applyLookup(self, lookup, polymer):
        result = []
        for i in range(len(polymer) - 1):
            pair = (polymer[i], polymer[i + 1])
            ruleOutput = lookup.get(pair)
            result.append(pair[0])
            if(ruleOutput != None):
                result.append(ruleOutput)
        result.append(polymer[len(polymer) - 1])
        return ''.join(result)

    def efficientIterate(self, stepSize, stepCount, polymer):
        lookup = self.createNStepLookup(stepSize)
        for i in range(stepCount):
            print(i)
            polymer = self.applyLookup(lookup, polymer)
        return polymer


def findMostAndLeastCommonCount(polymer):
    counts = {}
    for c in polymer:
        existingValue = counts.get(c, 0)
        counts.update({c: existingValue + 1})
    return Utility.maxBy(counts.items(), lambda item: item[1]), Utility.minBy(counts.items(), lambda item: item[1])


def findMostAndLeastCommonFromPairCount(pairCount):
    inputLines = Utility.getLinesFromFile(filePath)
    initialPolymer = inputLines[0]

    counts = {}
    for pair, count in pairCount.items():
        # Only update with left element of each pair to prevent double counting
        existingValue = counts.get(pair[0], 0)
        counts.update({pair[0]: existingValue + count})

    # add in last element of polymer (which will be last element of initial polymer) to compensate it not being a left element
    lastChar = initialPolymer[-1]
    existingValue = counts.get(lastChar, 0)
    counts.update({lastChar: existingValue + 1})

    return Utility.maxBy(counts.items(), lambda item: item[1]), Utility.minBy(counts.items(), lambda item: item[1])


def initializePairSetFromFile():
    inputLines = Utility.getLinesFromFile(filePath)
    polymer = inputLines[0]
    pairCount = {}
    for i in range(len(polymer) - 1):
        pL, pR = polymer[i:i+2]
        increasePairCount(pairCount, (pL, pR))
    return pairCount


def solvePart1():
    rules = Rules()
    inputLines = Utility.getLinesFromFile(filePath)
    polymer = inputLines[0]

    for i in range(10):
        polymer = rules.applyRules(polymer)

    mostCommon, leastCommon = findMostAndLeastCommonCount(polymer)

    print('Solution to part1:')
    print(polymer)
    print(mostCommon, leastCommon)
    print(mostCommon[1] - leastCommon[1])


def solvePart2():
    rules = Rules()
    pairCount = initializePairSetFromFile()

    for i in range(40):
        pairCount = rules.applyRulesToPairCount(pairCount)

    mostCommon, leastCommon = findMostAndLeastCommonFromPairCount(pairCount)

    print('Solution to part2:')
    print(mostCommon, leastCommon)
    print(mostCommon[1] - leastCommon[1])


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
