from __future__ import annotations
import Utility

filePath = 'input/day18/part1.txt'


class Number:
    def __init__(self) -> None:
        pass

    def initializeFromString(self, input: str, parent: Number, isLeftChild: bool):
        self.parent = parent
        self.isLeftChild = isLeftChild

        if(not input.startswith('[')):
            self.isRegularValue = True
            self.regularValue = int(input)
        else:
            self.isRegularValue = False
            innerSection = input[1:-1]
            middleIndex = 0
            if innerSection.startswith('['):
                index = 0
                bracketDepth = 1
                while(bracketDepth > 0):
                    index += 1
                    if (innerSection[index] == '['):
                        bracketDepth += 1
                    if (innerSection[index] == ']'):
                        bracketDepth -= 1

                # validation:
                if innerSection[index + 1] != ',':
                    raise Exception(
                        'left and right section should be split by ,')

                middleIndex = index + 1
            else:
                middleIndex = innerSection.find(',')

            leftSection = innerSection[0:middleIndex]
            rightSection = innerSection[middleIndex + 1:]

            leftChild = Number().initializeFromString(leftSection, self, True)
            rightChild = Number().initializeFromString(rightSection, self, False)
            self.children = [leftChild, rightChild]
        return self

    def initializeFromRegularValue(self, regularValue: int, parent: Number, isLeftChild: bool):
        self.isRegularValue = True
        self.regularValue = regularValue
        self.parent = parent
        self.isLeftChild = isLeftChild
        return self

    def initializeFromAddition(self, leftNumber: Number, rightNumber: Number):
        self.isRegularValue = False
        self.isLeftChild = None
        self.parent = None
        leftNumber.parent = self
        rightNumber.parent = self
        leftNumber.isLeftChild = True
        rightNumber.isLeftChild = False
        self.children = [leftNumber, rightNumber]
        return self

    def __repr__(self) -> str:
        if(self.isRegularValue):
            return self.regularValue.__repr__()

        leftChildRepr = self.children[0].__repr__()
        rightChildRepr = self.children[1].__repr__()

        return '[' + leftChildRepr + ',' + rightChildRepr + ']'

    def reduce(self):
        reduced = True
        while reduced:
            # print(self)
            reduced = self.attemptExplode() or self.attemptSplit()

    def attemptExplode(self, depth: int = 0) -> bool:
        if self.isRegularValue:
            return False

        if depth >= 4 and self.children[0].isRegularValue:
            # Rules guarantee that right child will also be regular value in case of explosion
            self.explodePair()
            return True

        return (self.children[0].attemptExplode(depth + 1)
                or self.children[1].attemptExplode(depth + 1))

    def explodePair(self):
        # To find left number, go up until we reach a parent of which we are the right
        # child, go to the left child and recurse on the right child until we reach a regular value
        c = self
        while((not c == None) and (c.isLeftChild)):
            c = c.parent

        if (c != None and c.parent != None):
            # If == None, no leftwise number exists to add to.
            c = c.parent
            c = c.children[0]
            while (not c.isRegularValue):
                c = c.children[1]

            # Found number to add left of exploding pair to
            c.regularValue += self.children[0].regularValue

        # Now do the same logic to find right adjacent number:
        c = self
        while((not c == None) and (not c.isLeftChild)):
            c = c.parent

        if (c != None and c.parent != None):
            # If == None, no rightwise number exists to add to.
            c = c.parent
            c = c.children[1]
            while (not c.isRegularValue):
                c = c.children[0]

            # Found number to add right of exploding pair to
            c.regularValue += self.children[1].regularValue

        self.isRegularValue = True
        self.regularValue = 0
        self.children = None
        pass

    def attemptSplit(self) -> bool:
        if self.isRegularValue:
            if self.regularValue > 9:
                self.split()
                return True
            return False

        return self.children[0].attemptSplit() or self.children[1].attemptSplit()

    def split(self):
        newLeftValue = self.regularValue // 2
        newRightValue = self.regularValue - newLeftValue
        self.regularValue = None
        self.isRegularValue = False
        leftChild = Number().initializeFromRegularValue(newLeftValue, self, True)
        rightChild = Number().initializeFromRegularValue(newRightValue, self, False)
        self.children = [leftChild, rightChild]

    def getMagnitude(self) -> int:
        if self.isRegularValue:
            return self.regularValue

        return 3 * self.children[0].getMagnitude() + 2 * self.children[1].getMagnitude()


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    currentSum = Number().initializeFromString(inputLines[0], None, None)
    for l in inputLines[1:]:
        nextNumber = Number().initializeFromString(l, None, None)
        currentSum = Number().initializeFromAddition(currentSum, nextNumber)
        currentSum.reduce()
        print()

    print('Solution to part1:')
    print(currentSum)
    print(currentSum.getMagnitude())


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    highestMagnitude = 0
    bestReducedSum = None
    for i in range(len(inputLines)):
        for j in range(len(inputLines)):
            if (i == j):
                continue
            leftNumber = Number().initializeFromString(inputLines[i], None, None)
            rightNumber = Number().initializeFromString(inputLines[j], None, None)
            sum = Number().initializeFromAddition(leftNumber, rightNumber)
            sum.reduce()
            if sum.getMagnitude() > highestMagnitude:
                highestMagnitude = sum.getMagnitude()
                bestReducedSum = sum

    print('Solution to part2:')
    print(bestReducedSum)
    print(highestMagnitude)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
