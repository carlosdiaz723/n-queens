import tkinter as tk
import time

# --------------------------------------------------
# UTILITY


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


def backtracking(board, col=0):
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
# RUNNERS


def singleRun():
    global n
    try:
        n = int(singleN.get())
        assert n >= 8
    except ValueError:
        print('N must be a valid integer')
        return
    except AssertionError:
        print('N must be GREATER THAN or EQUAL TO *8*')
        return

    isQueenBT = emptyBoard(size=n)
    t1 = time.time_ns()
    btSuccess = backtracking(isQueenBT)
    t2 = time.time_ns()
    btDelta = t2 - t1

    isQueenBB = emptyBoard(size=n)
    t1 = time.time_ns()
    bbSuccess = branchAndBound(isQueenBB)
    t2 = time.time_ns()
    bbDelta = t2 - t1

    print('\n\nFor N={}, \nBacktracking Solution (found '
          'in ~{} microseconds): '.format(n, round(btDelta/1000)))
    printBoard(isQueenBT)
    print('\nBranch and Bound Solution (found in ~{} micro'
          'seconds): '.format(round(bbDelta/1000)))
    printBoard(isQueenBB)


def rangeRun():
    try:
        n = list(range(int(leftN.get()), int(rightN.get()) + 1))
    except ValueError:
        print('Both the lower and upper bounds of N must be valid integers')
        return
    print(n)


def selectRun():
    # try:
    nList = str(selectN.get()).replace(' ', '').split(',')
    nInts = list()
    for i in nList:
        nInts.append(int(i))
    print(nInts)
    # except:


# --------------------------------------------------
# GUI

master = tk.Tk()
master.title('N-Queens')
master.option_add('*Font', 'Times 20')


s = 'Solve an N-Queens Puzzle (N > 7) using N ='
tk.Label(master, text=s).grid(row=0, column=0)
singleN = tk.Entry(master)
singleN.grid(row=0, column=1)
tk.Button(master, text='Submit', command=singleRun).grid(row=0, column=2)


tk.Label(master, text='or, using N from:').grid(row=1, column=0)
leftN = tk.Entry(master)
leftN.grid(row=1, column=1)
tk.Label(master, text=' to:').grid(row=1, column=2)
rightN = tk.Entry(master)
rightN.grid(row=1, column=3)
tk.Button(master, text='Submit', command=rangeRun).grid(row=1, column=4)

s = 'or, select specific values for N. Separate them with commas:'
tk.Label(master, text=s).grid(row=2, column=0)
selectN = tk.Entry(master)
selectN.grid(row=2, column=1)
tk.Button(master, text='Submit', command=selectRun).grid(row=2, column=2)

tk.mainloop()
# --------------------------------------------------
# MAIN
n = int()
'''
isQueen = emptyBoard(size=n)
if backtracking(isQueen):
    printBoard(isQueen)

isQueen = emptyBoard(size=n)
if branchAndBound(isQueen):
    printBoard(isQueen)
'''
