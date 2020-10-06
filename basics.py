from pprint import pprint as pretty
# this is a comment
# I import pprint because pretty() will be used in place of print()
# to output the 2D array in a prettier format

# python doesnt need to know the type if you just give it a value
n = 8

# create an empty list with
board = list()
# or
board = []


'''
this is a multiline comment

add n lists of n None's into board, effectively creating an n by n board
this is pretty complex and "pythonic", don't worry about it too much,
just know that the result is like a 2D array full of nothing
'''

'''
python for loops are actually for-each loops, so this loop is saying
for each integer i in the list [0, 1, 2, ..., n-1]:
it just so happens that we don't NEED i, we just need this to happen n times
'''
for i in range(n):
    board.append([None] * n)

# set a specifc tile
board[4][6] = 'queen'

'''
so we have a means of representing a chess board, 
lets make a more practical example using the concepts above
'''

n = 8

isQueen = list()

for i in range(n):
    isQueen.append([False] * n)
# now we have a board full of False's instead of None's


def flip(board, row, col):
    '''
    A method for flipping the state of a tile

    Define methods by using 'def' and the name, no return type needed

    You dont even need to specify what type the parameters are.
    in this case im asking for a board, row, and col, but im not saying
    what they should be (ints, strings, lists, etc)
    '''
    # if the element is a boolean, just flip whatever it currently is
    if type(board[row][col]) is bool:
        board[row][col] = not board[row][col]
    else:
        board[row][col] = True


pretty(isQueen)
# im gonna place some queens in a couple random spots
flip(isQueen, 0, 7)
flip(isQueen, 7, 5)
flip(isQueen, 4, 0)
flip(isQueen, 3, 1)
flip(isQueen, 6, 1)
flip(isQueen, 1, 2)
# print an empty line to separate the two pretty() results because
# all python print()'s are like println() unless otherwise specified
print()
pretty(isQueen)
print()

# a more common use of a for loop: print each tile in the first column
for row in isQueen:
    # here im going to print each tile BUT put a comma and space after instead
    # of the default newline
    print(row[0], end=', ')

print()
# or maybe print each tile in the last row
for tile in isQueen[n-1]:
    print(tile, end=', ')

print()
