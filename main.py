from pprint import pprint as pretty

n = 24
isQueen = list()

for i in range(n):
    isQueen.append([False] * n)


def flip(board, row, col):
    '''
    A method for flipping the state of a tile
    '''
    # if the element is a boolean, just flip whatever it currently is
    if type(board[row][col]) is bool:
        board[row][col] = not board[row][col]
    else:
        board[row][col] = True


def printBoard(board):
    for i in range(n):
        for j in range(n):
            if board[i][j]:
                print('Q', end=' ')
            else:
                print('#', end=' ')
        print()


def isSafePlace(board, row, col):
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
        if isSafePlace(board, i, col):
            board[i][col] = True
            if backtracking(board, col + 1):
                return True
            else:
                board[i][col] = False
    return False


if backtracking(isQueen, 0):
    printBoard(isQueen)
