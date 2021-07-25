#!/usr/bin/env python3.8
#
# Analyze the 12 ways to start a tic-tac-toe game and output winning games.
# I prevent the most obvious symmetric solutions from appearing more than
# once by preventing "repeated" boards in the first three moves.
#
# "1" is for the first player
# "2" is for the second player (temporarily called "4" in the code)
#
# When listing moves that were done...
# "10" is a block.
# The other numbers for the moves are...
#    1 2 3
#    4 5 6
#    7 8 9
# I don't list the first 2 moves in the starting board, nor do I show the
# final block (the way to win tic-tac-toe is to require the opponent to
# block two places at once).
# Note that these are temporarily 0-9 (not 1-10) in the code.
#
# I force players to win whenever there are 2 of their own in a line, and I
# force them to block whenever there are 2 of the other player's in a line.
# Winning takes priority over blocking!
#
# View the 12 starting boards below and choose the one you want, and set
# choice variable accordingly...
#  (1) 1st move is MIDDLE; 2nd is SIDE
#  (2) 1st move is MIDDLE; 2nd is CORNER
#  (3) 1st move is CORNER; 2nd is MIDDLE
#  (4) 1st move is CORNER; 2nd is ADJACENT SIDE
#  (5) 1st move is CORNER; 2nd is OPPOSITE SIDE
#  (6) 1st move is CORNER; 2nd is ADJACENT CORNER
#  (7) 1st move is CORNER; 2nd is OPPOSITE CORNER
#  (8) 1st move is SIDE; 2nd is MIDDLE
#  (9) 1st move is SIDE; 2nd is ADJACENT CORNER
#  (10) 1st move is SIDE; 2nd is OPPOSITE CORNER
#  (11) 1st move is SIDE; 2nd is ADJACENT SIDE
#  (12) 1st move is SIDE; 2nd is OPPOSITE SIDE


## set this!
choice = 4



# define start tic-tac-toe board
if choice==1:
  start = [0,0,0,
           2,1,0,
           0,0,0]
elif choice==2:
  start = [0,0,0,
           0,1,0,
           2,0,0]
elif choice==3:
  start = [0,0,0,
           0,2,0,
           1,0,0]
elif choice==4:
  start = [1,2,0,
           0,0,0,
           0,0,0]
elif choice==5:
  start = [1,0,0,
           0,0,2,
           0,0,0]
elif choice==6:
  start = [1,0,2,
           0,0,0,
           0,0,0]
elif choice==7:
  start = [0,0,1,
           0,0,0,
           2,0,0]
elif choice==8:
  start = [0,0,0,
           1,2,0,
           0,0,0]
elif choice==9:
  start = [2,1,0,
           0,0,0,
           0,0,0]
elif choice==10:
  start = [0,1,0,
           0,0,0,
           2,0,0]
elif choice==11:
  start = [0,1,0,
           2,0,0,
           0,0,0]
elif choice==12:
  start = [0,0,0,
           1,0,2,
           0,0,0]
else:
  print('invalid choice!')
  quit()



# print list as tic-tac-toe table
def myPrint(matrix):
  print('')
  print(matrix[0:3])
  print(matrix[3:6])
  print(matrix[6:9])
  print('\n')

# Turn history list into string.
# Python indexing starts at 0, so add 1 when printing.
def makeString(history):
  sHistory = ''
  for i in range(len(history)):
    sHistory += ' ' + str(history[i] + 1)
  return sHistory



print('\n'*10)
print('you chose board ' + str(choice) + '...')
myPrint(start)
print('\n\n')



# 8 rows of this are for the...
#          first 3 columns,           then the first 3 rows,     then the 2 diagonals
indices = ((0,3,6), (1,4,7), (2,5,8), (0,1,2), (3,4,5), (6,7,8), (0,4,8), (6,4,2))




# using 4 instead of 2 is useful for easily detecting wins (and when to block) using sum()
M = [4 if x==2 else x for x in start]


# the indices of locations that are still unfilled
spotsFree = [x for x in range(9) if start[x]==0]


# due to symmetry, I prevent certain moves from occurring on some boards
# If altering start list for choice 1, 2, 3, 7, 8, or 12,
#   be sure that iMaxStart covers all necessary situations.
if choice in (1,2,3,7,8,12):
  iMaxStart = 4
else:
  iMaxStart = 7



# recursive function
def searchForWins( M, spotsFree, iMax, history ):

  if len(history)%2 == 0:  # if length of history is even
    newValue = 1    # place a 1 instead of a 4 on the tic-tac-toe board
    blockCondition = 8  # if, let's say, sum(row) is 8, block
    winPlayer = '2'   # if, let's say, sum(column) is also 8, other player wins
  else:
    newValue = 4
    blockCondition = 2
    winPlayer = '1'

  #myPrint(M)
  #print(history)

  # sums[i] is the sum of indices[i] of M
  sums = [sum([M[x] for x in indices[y]]) for y in range(8)]
  if blockCondition in sums:   # block

      type = sums.index(blockCondition)
      ind = [x for x in indices[type] if M[x]==0][0]  # location to block

      M[ind] = newValue
      spotsFree.remove(ind)

      sums = [sum([M[x] for x in indices[y]]) for y in range(8)]
      if blockCondition in sums:  # win if there is another thing needing to be blocked!
          M[ind] = 0    # undo change to M
          M = [2 if x==4 else x for x in M]
          print('player ' + winPlayer + ' wins after' + makeString(history))
          myPrint(M)
      else:
          searchForWins( M, spotsFree, 6-len(history), history+[9] )

  else:
      for i in range(iMax):  #don't use len(spotsFree) instead of iMax

          # I must make copies because you can't pass by value in Python
          M2 = M[:]
          spotsFree2 = spotsFree[:]

          ii = spotsFree[i]  #the index of the piece to be added on new board
          M2[ii] = newValue  #add piece to new board
          del spotsFree2[i]  #update the new list of available moves

          searchForWins( M2, spotsFree2, 6-len(history), history+[ii] )



# do it!
searchForWins( M, spotsFree, iMaxStart, [] )

