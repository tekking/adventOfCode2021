import Utility
from functools import reduce
import operator

filePath = 'input/day16/part1.txt'


def getInputAsBinary():
    inputLines = Utility.getLinesFromFile(filePath)
    line = inputLines[0]
    resultArray = []
    for c in line:
        intValue = int(c, 16)
        resultArray.append(format(intValue, '04b'))
    return ''.join(resultArray)


class Packet:
    def __init__(self, binaryRepr) -> None:
        self.version = int(binaryRepr[0:3], 2)
        self.type = int(binaryRepr[3:6], 2)
        if(self.type == 4):
            # Literal packet
            self.parseLiteralValue(binaryRepr)
            pass
        else:
            self.lengthType = int(binaryRepr[6], 2)
            if(self.lengthType == 0):
                # total length mode
                self.parseContentLengthBytes(binaryRepr)
            else:
                # number of packets mode
                self.parseConentLengthPackets(binaryRepr)

    def parseLiteralValue(self, binaryRepr):  # returns # of bits consumed
        literalSection = binaryRepr[6:]
        index = 0
        valueReprArray = []
        while literalSection[index * 5] == '1':
            valueReprArray.append(literalSection[index * 5 + 1: index * 5 + 5])
            index += 1

        # add in last section (starting with 0 bit)
        valueReprArray.append(literalSection[index * 5 + 1: index * 5 + 5])
        valueRepr = ''.join(valueReprArray)
        self.literalValue = int(valueRepr, 2)
        self.totalLength = 6 + (index + 1) * 5

    # returns # of bits consumed
    def parseContentLengthBytes(self, binaryRepr):
        self.contentLengthInBytes = int(binaryRepr[7:22], 2)
        remainingContentSection = binaryRepr[22:]
        self.subPackets = []
        subPacketsLength = 0

        while(subPacketsLength < self.contentLengthInBytes):
            nextSubPacket = Packet(remainingContentSection)
            self.subPackets.append(nextSubPacket)
            subPacketsLength += nextSubPacket.totalLength
            remainingContentSection = remainingContentSection[nextSubPacket.totalLength:]

        if (subPacketsLength != self.contentLengthInBytes):
            raise Exception(
                'Mismatch while consuming subpackets in byte length')

        self.totalLength = 22 + subPacketsLength

    # returns # of bits consumed
    def parseConentLengthPackets(self, binaryRepr):
        self.contentLengthInPackets = int(binaryRepr[7:18], 2)
        remainingContentSection = binaryRepr[18:]
        self.subPackets = []
        consumedPackets = 0
        subPacketsLength = 0

        while(consumedPackets < self.contentLengthInPackets):
            nextSubPacket = Packet(remainingContentSection)
            self.subPackets.append(nextSubPacket)
            subPacketsLength += nextSubPacket.totalLength
            remainingContentSection = remainingContentSection[nextSubPacket.totalLength:]
            consumedPackets += 1

        self.totalLength = 18 + subPacketsLength

    def getVersionsSum(self) -> int:
        if(self.type == 4):
            return self.version
        else:
            subPacketsVersionSum = sum(
                map(lambda sp: sp.getVersionsSum(), self.subPackets))
            return subPacketsVersionSum + self.version

    def getValuesOfSubPackets(self) -> list[int]:
        return list(map(lambda sp: sp.evaluate(), self.subPackets))

    def evaluate(self) -> int:
        if self.type == 4:
            return self.literalValue

        subValues = self.getValuesOfSubPackets()

        if self.type == 0:
            return sum(subValues)

        if self.type == 1:
            return reduce(operator.mul, subValues)

        if self.type == 2:
            return Utility.minBy(subValues)

        if self.type == 3:
            return Utility.maxBy(subValues)

        if self.type == 5:
            if(subValues[0] > subValues[1]):
                return 1
            else:
                return 0

        if self.type == 6:
            if(subValues[0] < subValues[1]):
                return 1
            else:
                return 0

        if self.type == 7:
            if(subValues[0] == subValues[1]):
                return 1
            else:
                return 0



def solvePart1():
    input = getInputAsBinary()
    topLevel = Packet(input)

    print('Solution to part1:')
    print(topLevel.getVersionsSum())


def solvePart2():
    input = getInputAsBinary()
    topLevel = Packet(input)

    print('Solution to part2:')
    print(topLevel.evaluate())


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
