from pprint import pprint as pretty


# --------------------------------------------------
# UTILITY

def flip(board, row, col):
    '''
    A method for flipping the state of a tile
    '''
    # if the element is a boolean, just flip whatever it cuiently is
    if type(board[row][col]) is bool:
        board[row][col] = not board[row][col]
    else:
        board[row][col] = True


def emptyBoard(size):
    board = list()
    for _ in range(size):
        board.append([False] * size)
    return board


def printBoard(board):
    for i in range(n):
        for j in range(n):
            if board[i][j]:
                print('Q', end=' ')
            else:
                print('#', end=' ')
        print()

# --------------------------------------------------
# BACKTRACKING


def isSafeBT(board, row, col):
    for i in range(col):
        if board[row][i]:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j]:
            return False
    return True


def backtracking(board, col):
    if col >= n:
        return True

    for i in range(n):
        if isSafeBT(board, i, col):
            board[i][col] = True
            if backtracking(board, col + 1):
                return True
            else:
                board[i][col] = False
    return False

# --------------------------------------------------
# BRANCH AND BOUND


def isSafeBB(row, col, leftDiag, rightDiag, rowLookup,
             leftDiagLookup, rightDiagLookup):
    return not(leftDiagLookup[leftDiag[row][col]] or
               rightDiagLookup[rightDiag[row][col]] or
               rowLookup[row])


def branchAndBoundHelp(board, col, leftDiag, rightDiag,
                       rowLookup, leftDiagLookup,
                       rightDiagLookup):

    if col >= n:
        return True

    for i in range(n):
        if isSafeBB(i, col, leftDiag, rightDiag, rowLookup, leftDiagLookup,
                    rightDiagLookup):
            board[i][col] = True
            rowLookup[i] = True
            leftDiagLookup[leftDiag[i][col]] = True
            rightDiagLookup[rightDiag[i][col]] = True

            if(branchAndBoundHelp(board, col + 1, leftDiag, rightDiag,
                                  rowLookup, leftDiagLookup, rightDiagLookup)):
                return True

            board[i][col] = False
            rowLookup[i] = False
            leftDiagLookup[leftDiag[i][col]] = False
            rightDiagLookup[rightDiag[i][col]] = False

    return False


def branchAndBound(board):

    leftDiag = [[0 for i in range(n)] for j in range(n)]
    rightDiag = [[0 for i in range(n)] for j in range(n)]

    rowLookup = [False] * n
    leftDiagLookup = [False] * (2 * n - 1)
    rightDiagLookup = [False] * (2 * n - 1)

    for i in range(n):
        for j in range(n):
            leftDiag[i][j] = i + j
            rightDiag[i][j] = i - j + 7

    return branchAndBoundHelp(board, 0, leftDiag, rightDiag, rowLookup,
                              leftDiagLookup, rightDiagLookup)


# --------------------------------------------------
# MAIN
n = 24
'''isQueen = emptyBoard(size=n)
if backtracking(isQueen, 0):
    printBoard(isQueen)'''

isQueen = emptyBoard(size=n)
if branchAndBound(isQueen):
    printBoard(isQueen)
