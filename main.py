import tkinter as tk
import time
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# UTILITY

def emptyBoard(size):
    '''
    Returns an empty board
    (an NxN 2D Array where N=size and all values are set to False)
    '''
    board = list()
    for _ in range(size):
        board.append([False] * size)
    return board


def printBoard(board):
    '''
    Prints a board to the CLI by showing Queens as 'Q' and blank spaces as '#'
    '''
    for i in range(n):
        for j in range(n):
            if board[i][j]:
                print('Q', end=' ')
            else:
                print('#', end=' ')
        print()


# -----------------------------------------------------------------------------
# BACKTRACKING

def isSafeBT(board, row, col):
    '''
    Helper function used by the Backtracking (BT) algorithm
    Determines if a given placement is safe given the board's current state
    Returns True if safe, false otherwise

    NOTE: Only the left side of the current spot is checked since there are
    guaranteed no placements to the right of it. Also the column is not checked
    since there is necessarily only one Queen placed per column.
    '''
    # check all spaces to the left in the current row
    for i in range(col):
        if board[row][i]:
            return False
    # check upper left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False
    # check lower left diagonal
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j]:
            return False
    return True


def backtracking(board, col=0):
    # if reached end of board (falling off the right side)
    if col >= n:
        return True
    # run through each row in column
    for i in range(n):
        # if safe, place it
        if isSafeBT(board, i, col):
            board[i][col] = True
            # check to see if next column has safe move given current placement
            if backtracking(board, col + 1):
                return True
            # if next column has no valid move, remove queen
            else:
                board[i][col] = False
    # this is if somehow no solution is found
    # The code should never reach here (theoretically)
    return False


# -----------------------------------------------------------------------------
# BRANCH AND BOUND

def isSafeBB(row, col, leftDiag, rightDiag, rowLookup,
             leftDiagLookup, rightDiagLookup):
    '''
    Helper function used by the Branch and Bound (BB) algorithm
    Determines if a given placement is safe given the board's current state
    Returns True if safe, false otherwise.

    It determines this using the 3 preprocessed
    lookups and ensures all three are safe.
    '''
    return not(leftDiagLookup[leftDiag[row][col]] or
               rightDiagLookup[rightDiag[row][col]] or
               rowLookup[row])


def bbRecursive(board, col, leftDiag, rightDiag,
                rowLookup, leftDiagLookup,
                rightDiagLookup):
    '''
    The main recursive portion of the Branch and Bound algorithm
    '''
    # if reached end of board (falling off the right side)
    if col >= n:
        return True

    for i in range(n):
        if isSafeBB(i, col, leftDiag, rightDiag, rowLookup, leftDiagLookup,
                    rightDiagLookup):
            # place Queen
            board[i][col] = True
            # update lookup tables
            rowLookup[i] = True
            leftDiagLookup[leftDiag[i][col]] = True
            rightDiagLookup[rightDiag[i][col]] = True

            if(bbRecursive(board, col + 1, leftDiag, rightDiag,
                           rowLookup, leftDiagLookup, rightDiagLookup)):
                return True
            # the placement leads to a deadend, remove queen
            board[i][col] = False
            # undo lookup table adjustments
            rowLookup[i] = False
            leftDiagLookup[leftDiag[i][col]] = False
            rightDiagLookup[rightDiag[i][col]] = False
    # this is if somehow no solution is found
    # The code should never reach here (theoretically)
    return False


def branchAndBound(board):
    '''
    The setup for the Branch and Bound algortihm right before the recursive
    function is called. Here, the lookup tables are created and instantiated
    properly based off of N. This preprocessing is part of the reason why BB is
    much faster as N increases.
    '''
    leftDiag = [[0 for i in range(n)] for j in range(n)]
    rightDiag = [[0 for i in range(n)] for j in range(n)]
    rowLookup = [False] * n
    leftDiagLookup = [False] * (2 * n - 1)
    rightDiagLookup = [False] * (2 * n - 1)

    for i in range(n):
        for j in range(n):
            leftDiag[i][j] = i + j
            rightDiag[i][j] = i - j + (n - 1)

    return bbRecursive(board, 0, leftDiag, rightDiag, rowLookup,
                       leftDiagLookup, rightDiagLookup)


# -----------------------------------------------------------------------------
# RUNNERS

def singleRun():
    '''
    Runs when a single N is requested on the GUI. Prints the solution and time
    taken by both algorithms.
    '''
    # N refers to the global N that has already been instantiated
    global n
    # assert that the user input a valid integer N
    try:
        n = int(singleN.get())
        assert n >= 8
    except ValueError:
        print('N must be a valid integer')
        return
    except AssertionError:
        print('N must be GREATER THAN or EQUAL TO *8*')
        return

    # create empty board of size NxN for BT to manipulate
    isQueenBT = emptyBoard(size=n)
    # start clock
    t1 = time.perf_counter_ns()
    # run algorithm
    btSuccess = backtracking(isQueenBT)
    # ensure success
    assert btSuccess, 'Backtracking failed to find a solution'
    # stop clock
    t2 = time.perf_counter_ns()
    # record time taken
    btDelta = t2 - t1

    # repeat above process for BB
    isQueenBB = emptyBoard(size=n)
    t1 = time.perf_counter_ns()
    bbSuccess = branchAndBound(isQueenBB)
    assert bbSuccess, 'Branch and Bound failed to find a solution'
    t2 = time.perf_counter_ns()
    bbDelta = t2 - t1

    # print results to CLI
    print('\n\nFor N={}, \nBacktracking Solution (found '
          'in {:,} nanoseconds): '.format(n, btDelta))
    printBoard(isQueenBT)
    print('\nBranch and Bound Solution (found in {:,} nano'
          'seconds): '.format(bbDelta))
    printBoard(isQueenBB)


def rangeRun():
    '''
    Runs when a range of N is selected on the GUI.
    This is an indirect call to selectRun() since logically a range is just a
    special case of a select run. 
    '''
    # ensure that the lower and upper bounds are valid
    try:
        nList = list(range(int(leftN.get()), int(rightN.get()) + 1))
        assert int(rightN.get()) > int(leftN.get()) >= 8
    except ValueError:
        print('Invalid Range. Both the lower and upper bounds of N must be '
              'valid integers')
        return
    except AssertionError:
        print('Invalid Range. Lower bound must be >= 8, and upper bounds must '
              'be greater than the lower bound')
        return
    # pass the list of N's onto selectRun
    selectRun(nList)


def selectRun(range=None):
    '''
    Runs when a select group of N is chosen on the GUI.
    '''
    # N refers to the global N that has already been instantiated
    global n
    # create empty list to store the N's that need to be ran
    nInts = list()
    # if the method was called with a range, the cleaning work has already been
    # done by range() and the list of N's has already been determined
    if range is not None:
        nInts = range
    # otherwise, selectRun() was actually called by the GUI, so clean the input
    else:
        # remove spaces and then take each value thats separated by a comma
        try:
            nList = str(selectN.get()).replace(' ', '').split(',')
            nInts = list()
            # ensure each value is a valid integer
            for i in nList:
                assert int(i) >= 8
                nInts.append(int(i))
        except ValueError:
            print('Invalid sequence. Ensure only one comma between entries and'
                  ' that all entries are integers')
            return
        except AssertionError:
            print('Invalid sequence. All values for N must be GREATER THAN '
                  'or EQUAL TO *8*')
            return

    # lists to store the times taken for each algorithm on each N
    bbTimes, btTimes = list(), list()

    # for each N, essentially run the same algorithm as singleRun()
    for i in nInts:
        # update global i
        n = i
        # single run for BT
        isQueenBT = emptyBoard(size=n)
        t1 = time.perf_counter_ns()
        btSuccess = backtracking(isQueenBT)
        assert btSuccess, 'Backtracking failed to find a solution '\
                          'for n={}'.format(n)
        t2 = time.perf_counter_ns()
        btDelta = t2 - t1
        # store the time taken
        btTimes.append(btDelta)

        # single run for BB
        isQueenBB = emptyBoard(size=n)
        t1 = time.perf_counter_ns()
        bbSuccess = branchAndBound(isQueenBB)
        assert bbSuccess, 'Branch and Bound failed to find a solution '\
                          'for n={}'.format(n)
        t2 = time.perf_counter_ns()
        bbDelta = t2 - t1
        # store the time taken
        bbTimes.append(bbDelta)

        # print results to CLI
        print('\n\nFor N={}, \nBacktracking Solution (found '
              'in {:,} nanoseconds): '.format(n, btDelta))
        printBoard(isQueenBT)
        print('\nBranch and Bound Solution (found in {:,} nano'
              'seconds): '.format(bbDelta))
        printBoard(isQueenBB)
    # pass the "time taken" data onto the graphing method
    showGraphs(nInts, btTimes, bbTimes)


# -----------------------------------------------------------------------------
# OUTPUT GRAPHS

def showGraphs(x, y1, y2):
    '''
    Creates and shows a graph of the Times Taken for each N by both algorithms 
    '''
    # instantiate plot
    _, ax = plt.subplots()
    # plot the BT times
    ax.plot(x, y1, label='BackTracking')
    # plot the BB times
    ax.plot(x, y2, label='Branch and Bound')
    # set graph title and labels
    ax.set(xlabel='N',
           ylabel='Time Taken (nanoseconds)',
           title='Time Taken as N Increases')
    # place legend to see which color corresponds to which algorithm
    plt.legend(loc='upper left')
    # show graph
    plt.show()


# -----------------------------------------------------------------------------
# GUI

# instantiate window
master = tk.Tk()
master.title('N-Queens')
master.option_add('*Font', 'Times 20')

# labels and entries for single N use
s = 'Solve an N-Queens Puzzle (N >= 8) using N ='
tk.Label(master, text=s).grid(row=0, column=0)
singleN = tk.Entry(master)
singleN.grid(row=0, column=1)
tk.Button(master, text='Submit', command=singleRun).grid(row=0, column=2)

# labels and entries for range of N use
tk.Label(master, text='or, using N from:').grid(row=1, column=0)
leftN = tk.Entry(master)
leftN.grid(row=1, column=1)
tk.Label(master, text=' to:').grid(row=1, column=2)
rightN = tk.Entry(master)
rightN.grid(row=1, column=3)
tk.Button(master, text='Submit', command=rangeRun).grid(row=1, column=4)

# labels and entries for select N use
s = 'or, select specific values for N. Separate them with commas:'
tk.Label(master, text=s).grid(row=2, column=0)
selectN = tk.Entry(master)
selectN.grid(row=2, column=1)
tk.Button(master, text='Submit', command=selectRun).grid(row=2, column=2)

# instantiate global N and run GUI
n = int()
tk.mainloop()
