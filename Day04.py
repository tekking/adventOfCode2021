import Utility

filePath = 'input/day04/part1.txt'


class Board:
    def __init__(self, inputLinesForBoard: list[str]) -> None:
        self.rows = [list(range(5)) for i in range(5)]
        self.marked = [[0 for j in range(5)] for i in range(5)]
        for i, line in enumerate(inputLinesForBoard):
            for j in range(5):
                value = int(line[j*3: j*3+2])
                self.rows[i][j] = value

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.rows.__str__() + '\n' + self.marked.__str__()

    def hasWon(self) -> bool:
        for i in range(5):
            if(sum(map(lambda j: self.marked[i][j], range(5))) == 5):
                return True
            if(sum(map(lambda j: self.marked[j][i], range(5))) == 5):
                return True
        return False

    def markNumber(self, number: int) -> None:
        for i in range(5):
            for j in range(5):
                if(self.rows[i][j] == number):
                    self.marked[i][j] = 1

    def getScore(self) -> int:
        sum = 0
        for i in range(5):
            for j in range(5):
                if(self.marked[i][j] == 0):
                    sum += self.rows[i][j]
        return sum


def getNumbersFromInput(numbersLine: str) -> list[int]:
    return list(map(int, numbersLine.split(',')))


def getBoardsFromInput(boardInputLines: list[str]) -> list[Board]:
    boards = []
    while(len(boardInputLines) > 0):
        boards.append(Board(boardInputLines[:5]))
        boardInputLines = boardInputLines[6:]
    return boards


def findWinningNumberAndBoard(numbers: list[int], boards: list[Board]) -> tuple[int, Board]:
    for number in numbers:
        for board in boards:
            board.markNumber(number)
            if(board.hasWon()):
                return number, board


def findLastWinningBoardAndNumber(numbers: list[int], boards: list[Board]) -> tuple[int, Board]:
    remainingBoards = boards.copy()

    for number in numbers:
        boardsToLoop = remainingBoards.copy()
        for board in boardsToLoop:
            board.markNumber(number)
            if(board.hasWon()):
                if(len(remainingBoards) == 1):
                    return number, remainingBoards[0]
                remainingBoards.remove(board)


def solvePart1():
    inputLines = Utility.getLinesFromFile(filePath)
    numbers = getNumbersFromInput(inputLines[0])
    boards = getBoardsFromInput(inputLines[2:])

    winningNumber, winningBoard = findWinningNumberAndBoard(numbers, boards)

    print('Solution to part1:')
    print(winningBoard.getScore() * winningNumber)


def solvePart2():
    inputLines = Utility.getLinesFromFile(filePath)
    numbers = getNumbersFromInput(inputLines[0])
    boards = getBoardsFromInput(inputLines[2:])

    losingNumber, losingBoard = findLastWinningBoardAndNumber(numbers, boards)

    print('Solution to part2:')
    print(losingBoard.getScore() * losingNumber)


if(__name__ == '__main__'):
    solvePart1()
    solvePart2()
