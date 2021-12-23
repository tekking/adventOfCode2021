from __future__ import annotations
from os import stat
import Utility
import bisect

# 'turn':
#   1: Check if any amphi can move into its final room
#   2: Move a amphi from its start into a hallway position
#   No other possible moves?
#   This implemntation became horror...
#   runtime part2 = ~2 min, probably very suboptimal

filePath = 'input/day23/part1.txt'

class State:
    def __init__(self) -> None:
        pass

    def initializeFromInput(self) -> State:
        inputLines = Utility.getLinesFromFile(filePath)
        roomLines = inputLines[2:4]
        positions = set()

        for i in range(2):
            for j in range(3, 10, 2):
                positions.add((roomLines[i][j], j + 4 + i))

        self.places = ['.' for i in range(15)]
        for p in positions:
            self.places[p[1]] = p[0]

        self.cost = 0
        return self

    def positionIsOccupied(self, position: int) -> bool:
        return self.places[position] != '.'

    def getTargetRoom(self, letter) -> int:
        # naive
        targetRoom = 3
        if(letter == 'B'):
            targetRoom = 4
        elif (letter == 'C'):
            targetRoom = 5
        elif (letter == 'D'):
            targetRoom = 6
        return targetRoom

    def getCostMultiplier(self, letter) -> int:
        # naive
        targetRoom = 1
        if(letter == 'B'):
            targetRoom = 10
        elif (letter == 'C'):
            targetRoom = 100
        elif (letter == 'D'):
            targetRoom = 1000
        return targetRoom

    def canFinishFromHallway(self, letter: str, hallwayPosition: int) -> tuple[bool, int, int]:
        targetRoom = self.getTargetRoom(letter)
        topPositionInRoom = targetRoom * 2 + 1
        bottomPositionInRoom = targetRoom * 2 + 2

        if (self.positionIsOccupied(topPositionInRoom)):
            # can't enter if top place is occupied
            return (False, 999999, -1)

        if (self.positionIsOccupied(bottomPositionInRoom) and self.places[bottomPositionInRoom] != letter):
            # can't enter if wrong letter is in room
            return (False, 999999, -1)

        upLeft = targetRoom - 2
        upRight = upLeft + 1

        cost = 0

        # move to adjacent hallway position
        if hallwayPosition <= upLeft:
            while(hallwayPosition < upLeft):
                cost += 1 if hallwayPosition == 0 else 2
                hallwayPosition += 1
                if(self.positionIsOccupied(hallwayPosition)):
                    return (False, 999999, -1)
        else:
            while(hallwayPosition > upRight):
                cost += 1 if hallwayPosition == 6 else 2
                hallwayPosition -= 1
                if(self.positionIsOccupied(hallwayPosition)):
                    return (False, 999999, -1)

        # add cost to move from hallwayPosition to room
        cost += 2
        multiplier = self.getCostMultiplier(letter)

        # add cost to move to back (if free):
        if(not self.positionIsOccupied(bottomPositionInRoom)):
            return (True, (cost + 1) * multiplier, bottomPositionInRoom)
        else:
            return (True, cost * multiplier, topPositionInRoom)

    def getHallwayPositionMovesFromRoom(self, roomNumber) -> list[tuple[int, int]]:
        if (not self.positionIsOccupied(roomNumber)):
            return []

        # Room numbers are 7/8 for left room, 9/10 for room next to that etc
        if (roomNumber % 2 == 0 and self.positionIsOccupied(roomNumber - 1)):
            return []

        letter = self.places[roomNumber]

        # Don't move from correct room unless there is a wrong letter below
        targetRoom = self.getTargetRoom(letter)
        if ((roomNumber - 1) // 2 == targetRoom and self.places[targetRoom * 2 + 2] == letter):
            return []

        costMultiplier = self.getCostMultiplier(letter)
        costModifier = 0 if roomNumber % 2 == 1 else 1
        possibleMoves = []
        upLeft = ((roomNumber - 1) // 2) - 2
        upRight = upLeft + 1

        upLeftCost = 2 + costModifier
        upRightCost = 2 + costModifier
        while(not self.positionIsOccupied(upLeft) and upLeft >= 0):
            possibleMoves.append((upLeft, upLeftCost * costMultiplier))
            upLeft -= 1
            upLeftCost += 2 if upLeft > 0 else 1

        while(not self.positionIsOccupied(upRight) and upRight <= 6):
            possibleMoves.append((upRight, upRightCost * costMultiplier))
            upRight += 1
            upRightCost += 2 if upRight < 6 else 1

        return possibleMoves

    def iterateFromState(self) -> list[State]:
        newStates = []
        for roomPosition in range(7, 15):
            moves = self.getHallwayPositionMovesFromRoom(roomPosition)
            for target, cost in moves:
                letter = self.places[roomPosition]
                newState = State()
                newState.cost = self.cost + cost
                newState.places = self.places.copy()
                newState.places[roomPosition] = '.'
                newState.places[target] = letter

                # only return max finished places as optimization
                newState.finishWherePossible()
                newStates.append(newState)

        return newStates

    def finishWherePossible(self):
        looping = True
        while(looping):
            looping = False
            for hallwayPosition in range(7):
                # check if any letter is in a hallway position and can finish
                letter = self.places[hallwayPosition]
                if letter == '.':
                    continue
                canFinish, cost, roomPosition = self.canFinishFromHallway(
                    letter, hallwayPosition)
                if canFinish:
                    looping = True
                    self.places[hallwayPosition] = '.'
                    self.places[roomPosition] = letter
                    self.cost += cost

    def getPlaceIcon(self, position) -> str:
        return self.places[position]

    def isFinished(self) -> bool:
        for roomPosition in range(7, 15):
            letter = self.places[roomPosition]
            if letter == '.':
                return False
            targetRoom = self.getTargetRoom(letter)
            if (roomPosition - 1) // 2 != targetRoom:
                return False
        return True

    def equalsPlaces(self, other: State) -> bool:
        for i, l in enumerate(self.places):
            if other.places[i] != l:
                return False

        return True

    def placesRepr(self) -> str:
        return ''.join(self.places)

    def __repr__(self) -> str:
        lines = []
        lines.append(''.join('#' for i in range(13)))
        lines.append('\n')
        hallway = '#' + self.getPlaceIcon(0) + ''.join(self.getPlaceIcon(i) + '.' for i in range(
            1, 5)) + self.getPlaceIcon(5) + self.getPlaceIcon(6) + '#'
        lines.append(hallway)
        lines.append('\n')
        topRooms = '###' + \
            ''.join(self.getPlaceIcon(i) + '#' for i in range(7, 14, 2)) + '##'
        lines.append(topRooms)
        lines.append('\n')
        bottomRooms = '  #' + \
            ''.join(self.getPlaceIcon(i) + '#' for i in range(8, 15, 2)) + '  '
        lines.append(bottomRooms)
        lines.append('\n')
        return ''.join(lines)


class DeeperState:
    def __init__(self) -> None:
        pass

    def initializeFromInput(self) -> State:
        inputLines = Utility.getLinesFromFile(filePath)
        roomLines = inputLines[2:4]
        positions = set()

        for i in range(2):
            for j in range(4):
                positions.add((roomLines[i][j * 2 + 3], j * 4 + 7 + (i * 3)))

        positions.add(('D', 8))
        positions.add(('D', 9))
        positions.add(('C', 12))
        positions.add(('B', 13))
        positions.add(('B', 16))
        positions.add(('A', 17))
        positions.add(('A', 20))
        positions.add(('C', 21))

        self.places = ['.' for i in range(23)]
        for p in positions:
            self.places[p[1]] = p[0]

        self.cost = 0
        return self

    def positionIsOccupied(self, position: int) -> bool:
        return self.places[position] != '.'

    def getTargetRoomContainer(self, letter) -> int:
        # naive
        targetRoom = 1
        if(letter == 'B'):
            targetRoom = 2
        elif (letter == 'C'):
            targetRoom = 3
        elif (letter == 'D'):
            targetRoom = 4
        return targetRoom

    def getCostMultiplier(self, letter) -> int:
        # naive
        targetRoom = 1
        if(letter == 'B'):
            targetRoom = 10
        elif (letter == 'C'):
            targetRoom = 100
        elif (letter == 'D'):
            targetRoom = 1000
        return targetRoom

    def canFinishFromHallway(self, letter: str, hallwayPosition: int) -> tuple[bool, int, int]:
        targetRoom = self.getTargetRoomContainer(letter)
        topPositionInRoom = targetRoom * 4 + 3

        if (self.positionIsOccupied(topPositionInRoom)):
            # can't enter if top place is occupied
            return (False, 999999, -1)

        # can't enter if wrong letter is anywhere in room
        for d in range(1, 4):
            pos = topPositionInRoom + d
            if (self.positionIsOccupied(pos) and self.places[pos] != letter):
                return (False, 999999, -1)

        upLeft = targetRoom
        upRight = upLeft + 1

        cost = 0

        # move to adjacent hallway position
        if hallwayPosition <= upLeft:
            while(hallwayPosition < upLeft):
                cost += 1 if hallwayPosition == 0 else 2
                hallwayPosition += 1
                if(self.positionIsOccupied(hallwayPosition)):
                    return (False, 999999, -1)
        else:
            while(hallwayPosition > upRight):
                cost += 1 if hallwayPosition == 6 else 2
                hallwayPosition -= 1
                if(self.positionIsOccupied(hallwayPosition)):
                    return (False, 999999, -1)

        # add cost to move from hallwayPosition to room
        cost += 2
        multiplier = self.getCostMultiplier(letter)

        # add cost to move to back (if free):
        costExtra = 0
        targetPos = topPositionInRoom
        while(targetPos < topPositionInRoom + 3 and (not self.positionIsOccupied(targetPos + 1))):
            targetPos += 1
            costExtra += 1

        return (True, (cost + costExtra) * multiplier, targetPos)

    def getRoomContainerOfRoom(self, roomNumber: int) -> int:
        return (roomNumber - 3) // 4

    def getHallwayPositionMovesFromRoom(self, roomNumber) -> list[tuple[int, int]]:
        if (not self.positionIsOccupied(roomNumber)):
            return []

        # Can only move if all higher rooms are free
        roomContainer = self.getRoomContainerOfRoom(roomNumber)
        topPositionInRoom = roomContainer * 4 + 3
        for inBetween in range(topPositionInRoom, roomNumber):
            if self.positionIsOccupied(inBetween):
                return []

        letter = self.places[roomNumber]

        # Don't move from correct room unless there is a wrong letter below
        targetRoom = self.getTargetRoomContainer(letter)
        if (roomContainer == targetRoom and self.places[targetRoom * 2 + 2] != letter):
            allCorrect = True
            for below in range(roomNumber + 1, topPositionInRoom + 4):
                if self.places[below] != letter:
                    allCorrect = False
                    break
            if allCorrect:
                return []

        costMultiplier = self.getCostMultiplier(letter)
        costModifier = roomNumber - topPositionInRoom
        possibleMoves = []
        upLeft = roomContainer
        upRight = upLeft + 1

        upLeftCost = 2 + costModifier
        upRightCost = 2 + costModifier
        while(not self.positionIsOccupied(upLeft) and upLeft >= 0):
            possibleMoves.append((upLeft, upLeftCost * costMultiplier))
            upLeft -= 1
            upLeftCost += 2 if upLeft > 0 else 1

        while(not self.positionIsOccupied(upRight) and upRight <= 6):
            possibleMoves.append((upRight, upRightCost * costMultiplier))
            upRight += 1
            upRightCost += 2 if upRight < 6 else 1

        return possibleMoves

    def iterateFromState(self) -> list[DeeperState]:
        newStates = []
        for roomPosition in range(7, 23):
            moves = self.getHallwayPositionMovesFromRoom(roomPosition)
            for target, cost in moves:
                letter = self.places[roomPosition]
                newState = DeeperState()
                newState.cost = self.cost + cost
                newState.places = self.places.copy()
                newState.places[roomPosition] = '.'
                newState.places[target] = letter

                # only return max finished places as optimization
                newState.finishWherePossible()
                newStates.append(newState)

        return newStates

    def finishWherePossible(self):
        looping = True
        while(looping):
            looping = False
            for hallwayPosition in range(7):
                # check if any letter is in a hallway position and can finish
                letter = self.places[hallwayPosition]
                if letter == '.':
                    continue
                canFinish, cost, roomPosition = self.canFinishFromHallway(
                    letter, hallwayPosition)
                if canFinish:
                    looping = True
                    self.places[hallwayPosition] = '.'
                    self.places[roomPosition] = letter
                    self.cost += cost

    def getPlaceIcon(self, position) -> str:
        return self.places[position]

    def isFinished(self) -> bool:
        for roomPosition in range(7, 23):
            letter = self.places[roomPosition]
            if letter == '.':
                return False
            targetRoomContainer = self.getTargetRoomContainer(letter)
            container = self.getRoomContainerOfRoom(roomPosition)
            if container != targetRoomContainer:
                return False
        return True

    def equalsPlaces(self, other: State) -> bool:
        for i, l in enumerate(self.places):
            if other.places[i] != l:
                return False

        return True

    def placesRepr(self) -> str:
        return ''.join(self.places)

    def __repr__(self) -> str:
        lines = []
        lines.append(''.join('#' for i in range(13)))
        lines.append('\n')
        hallway = '#' + self.getPlaceIcon(0) + ''.join(self.getPlaceIcon(i) + '.' for i in range(
            1, 5)) + self.getPlaceIcon(5) + self.getPlaceIcon(6) + '#'
        lines.append(hallway)
        lines.append('\n')
        topRooms = '###' + \
            ''.join(self.getPlaceIcon(i) + '#' for i in range(7, 20, 4)) + '##'
        lines.append(topRooms)
        lines.append('\n')
        for r in range(1, 4):
            roomRow = '  #' + \
            ''.join(self.getPlaceIcon(i) + '#' for i in range(7 + r, 20 + r, 4)) + '  '
            lines.append(roomRow)
            lines.append('\n')
        return ''.join(lines)

def solvePart1():
    return
    startState = State().initializeFromInput()
    stateCandidates = [startState]
    bestFinishCost = 99999999999

    passedStates = {startState.placesRepr(): 0}

    while(True):
        if len(stateCandidates) == 0:
            break
        cheapestState = Utility.minBy(
            stateCandidates, lambda state: state.cost)
        stateCandidates.remove(cheapestState)

        if cheapestState.cost > bestFinishCost:
            break

        newStates = cheapestState.iterateFromState()
        for n in newStates:
            if n.isFinished():
                if n.cost < bestFinishCost:
                    bestFinishCost = n.cost
                    print(bestFinishCost)
            else:
                pRepr = n.placesRepr()
                knownCost = passedStates.get(pRepr, 9999999999)
                if n.cost < knownCost:
                    stateCandidates.append(n)
                    passedStates.update({pRepr: n.cost})

    print('Solution to part1:')
    print(bestFinishCost)


def solvePart2():
    startState = DeeperState().initializeFromInput()
    stateCandidates = [startState]
    bestFinishCost = 99999999999

    passedStates = {startState.placesRepr(): 0}

    printCount = 0
    while(True):
        if len(stateCandidates) == 0:
            break
        cheapestState = Utility.minBy(
            stateCandidates, lambda state: state.cost)
        stateCandidates.remove(cheapestState)
        
        stateRepr = cheapestState.placesRepr()
        knownCost = passedStates.get(stateRepr, 9999999999)
        if knownCost < cheapestState.cost:
            continue

        printCount += 1
        if printCount % 100 == 0:
            print(cheapestState.cost)

        if cheapestState.cost > bestFinishCost:
            break

        newStates = cheapestState.iterateFromState()
        for n in newStates:
            if n.isFinished():
                if n.cost < bestFinishCost:
                    bestFinishCost = n.cost
                    print(bestFinishCost)
            else:
                pRepr = n.placesRepr()
                knownCost = passedStates.get(pRepr, 9999999999)
                if n.cost < knownCost:
                    stateCandidates.append(n)
                    passedStates.update({pRepr: n.cost})

    print('Solution to part2:')
    print(bestFinishCost)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
