from pprint import pprint as pretty

n = 8
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
