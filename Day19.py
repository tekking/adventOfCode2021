from __future__ import annotations
import Utility

filePath = 'input/day19/part1.txt'


def compareHashes(leftHashes: list[int], rightHashes: list[int], threshold: int) -> bool:
    matches = 0
    for l in leftHashes:
        if l in rightHashes:
            matches += 1
    return matches >= threshold


def getMatchingIndices(leftHashes: list[int], rightHashes: list[int]) -> list[int]:
    indices = []
    for i, l in enumerate(leftHashes):
        if l in rightHashes:
            indices.append(i)
    return indices


class Scanner:
    def __init__(self, inputLines: list[str]) -> None:
        self.name = inputLines[0].split('---')[1]
        self.measurements: list[tuple[int, int, int]] = []
        for l in inputLines[1:]:
            x, y, z = list(map(int, l.split(',')))
            self.measurements.append((x, y, z))
        self.buildDiffHashMatrix()

    def buildDiffHashMatrix(self):
        self.diffMatrix = []
        for left in self.measurements:
            hashes = []
            for right in self.measurements:
                axisDiffs = [abs(left[0] - right[0]),
                             abs(left[1] - right[1]),
                             abs(left[2] - right[2])]
                sortedAxisDiffs = sorted(axisDiffs)
                hash = sortedAxisDiffs[0] + 1000 * \
                    sortedAxisDiffs[1] + 1000000 * sortedAxisDiffs[2]
                hashes.append(hash)
            self.diffMatrix.append(hashes)

    def checkForMatch(self, other: Scanner) -> bool:
        for ownHashes in self.diffMatrix:
            for otherHashes in other.diffMatrix:
                if compareHashes(ownHashes, otherHashes, 12):
                    return True
        return False

    # returns the offset for use in determining scanner distance
    def adjustToOtherCoordinateSystem(self, other: Scanner) -> tuple[int, int, int]:
        matchingPairs = self.findMatchingNodeIndicesSet(other)

        # strategy: find correct mapping of axis (fe 0 -> 0, 1 -> 2, 2 -> 1)
        # and find correct orientation on each (* -1 or 1)
        # based on diffs between [0] and [n] in each Scanner
        # then finally determine the offset
        self.adjustAxisMapping(other, matchingPairs)
        return self.adjustOffset(other, matchingPairs)

    def adjustAxisMapping(self, other: Scanner, matchingPairs: list[tuple[int, int]]):
        basePair = matchingPairs[0]
        ownBaseNode, otherBaseNode = self.measurements[basePair[0]
                                                       ], other.measurements[basePair[1]]
        coordinateMappingMatches = [[0 for i in range(3)] for i in range(3)]
        targetDirectionMatches = [0 for i in range(3)]

        for ownI, otherI in matchingPairs[1:]:
            ownNode, otherNode = self.measurements[ownI], other.measurements[otherI]
            ownDiffs = [ownBaseNode[0] - ownNode[0],
                        ownBaseNode[1] - ownNode[1],
                        ownBaseNode[2] - ownNode[2]]
            otherDiffs = [otherBaseNode[0] - otherNode[0],
                          otherBaseNode[1] - otherNode[1],
                          otherBaseNode[2] - otherNode[2]]
            for i in range(3):
                for j in range(3):
                    if abs(ownDiffs[i]) == abs(otherDiffs[j]):
                        coordinateMappingMatches[j][i] += 1
                        if ownDiffs[i] == otherDiffs[j]:
                            targetDirectionMatches[j] += 1

        mapping = []
        for targetRow in coordinateMappingMatches:
            max = Utility.maxBy(targetRow)
            if max != len(matchingPairs) - 1:
                raise Exception(
                    'Did not find axis mapping that satisfies all diffs')
            if targetRow[0] == max:
                mapping.append(0)
            if targetRow[1] == max:
                mapping.append(1)
            if targetRow[2] == max:
                mapping.append(2)

        multipliers = []
        for j in range(3):
            if targetDirectionMatches[j] == len(matchingPairs) - 1:
                multipliers.append(1)
            else:
                multipliers.append(-1)

        newMeasurements = list(
            map(lambda m:
                (multipliers[0] * m[mapping[0]],
                 multipliers[1] * m[mapping[1]],
                 multipliers[2] * m[mapping[2]]),
                self.measurements))
        self.measurements = newMeasurements

    # returns the offset for use in determining scanner distance
    def adjustOffset(self, other: Scanner, matchingPairs: list[tuple[int, int]]):
        basePair = matchingPairs[0]
        ownBaseNode, otherBaseNode = self.measurements[basePair[0]
                                                       ], other.measurements[basePair[1]]
        xDiff = otherBaseNode[0] - ownBaseNode[0]
        yDiff = otherBaseNode[1] - ownBaseNode[1]
        zDiff = otherBaseNode[2] - ownBaseNode[2]

        newMeasurements = list(
            map(lambda m: (m[0] + xDiff, m[1] + yDiff, m[2] + zDiff),
                self.measurements))
        self.measurements = newMeasurements
        return (xDiff, yDiff, zDiff)

    def findMatchingNodeIndicesSet(self, other: Scanner) -> list[tuple[int, int]]:
        for ownHashes in self.diffMatrix:
            for otherHashes in other.diffMatrix:
                if compareHashes(ownHashes, otherHashes, 12):
                    pairs: list[tuple[int, int]] = []
                    for i, ownHash in enumerate(ownHashes):
                        for j, otherHash in enumerate(otherHashes):
                            if ownHash == otherHash:
                                pairs.append((i, j))
                    return pairs

    def __repr__(self) -> str:
        resultArray = []
        resultArray.append(f'--- {self.name} ---\n')
        resultArray.extend(
            map(lambda x: x.__repr__() + '\n', self.measurements))
        return ''.join(resultArray)


def splitInputToScanners() -> list[Scanner]:
    inputLines = Utility.getLinesFromFile(filePath)
    scannerLines = []
    scanners = []
    for l in inputLines:
        if l == '':
            scanners.append(Scanner(scannerLines))
            scannerLines = []
        else:
            scannerLines.append(l)

    scanners.append(Scanner(scannerLines))
    return scanners

# return scanner coordinates
def adjustScannersToFrameOfScannerZero(scanners: list[Scanner]) -> list[tuple[int, int, int]]:
    adjustedScanners = scanners[0:1].copy()
    unadjustedScanners = scanners[1:].copy()
    scannerCoordinates = []
    while(len(unadjustedScanners) > 0):
        for adjusted in adjustedScanners:
            for unadjusted in unadjustedScanners:
                if adjusted.checkForMatch(unadjusted):
                    offset = unadjusted.adjustToOtherCoordinateSystem(adjusted)
                    scannerCoordinates.append(offset)
                    unadjustedScanners.remove(unadjusted)
                    adjustedScanners.append(unadjusted)
                    #print(f'Adjusted {unadjusted.name} to {adjusted.name}')
                    break
    return scannerCoordinates

def findUniqueBeacons(scanners: list[Scanner]):
    beaconsSet = set()
    for s in scanners:
        for m in s.measurements:
            beaconsSet.add(m)
    return beaconsSet

def findLargestManhattan(points: list[tuple[int, int, int]]):
    largestDistance = 0
    for l in points:
        for r in points:
            dist = abs(l[0] - r[0]) + abs(l[1] - r[1]) + abs(l[2] - r[2])
            if dist > largestDistance:
                largestDistance = dist
    return largestDistance

def solvePart1():
    scanners = splitInputToScanners()
    adjustScannersToFrameOfScannerZero(scanners)
    uniqueBeacons = findUniqueBeacons(scanners)
    print('Solution to part1:')
    print(len(uniqueBeacons))


def solvePart2():
    scanners = splitInputToScanners()
    scannerCoordinates = adjustScannersToFrameOfScannerZero(scanners)
    print('Solution to part2:')
    print(findLargestManhattan(scannerCoordinates))


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
