#!/usr/bin/env python3.8
#
# Given a Tic-tac-toe board, analyze the consequences of all possible next moves
#
# The numbers for the locations are...
#    1 2 3
#    4 5 6
#    7 8 9
# Note that these are temporarily 0-8 (not 1-9) in the code.
#
# I force players to win whenever there are 2 of their own in a line, and I
# force them to block whenever there are 2 of the other player's in a line.
# Winning takes priority over blocking!


# Enter Tic-tac-toe board here...
#   0 is for unfilled square
#   1 is for the first player
#   2 is for the second player (temporarily called "4" in the code)

start = [0,0,0,
         1,0,2,
         0,1,0]




# check start[] for basic errors
n0 = 0
n1 = 0
n2 = 0
for i in start:
  if i==0:
    n0 += 1
  elif i==1:
    n1 += 1
  elif i==2:
    n2 += 1
if n0+n1+n2 != 9 or len(start) != 9 or n2 > n1 or (n1 - n2) > 1 or n0==0:
  print('  error: invalid start[]')
  exit()



# 8 rows of this are for the...
#          first 3 columns,           then the first 3 rows,     then the 2 diagonals
indices = ((0,3,6), (1,4,7), (2,5,8), (0,1,2), (3,4,5), (6,7,8), (0,4,8), (6,4,2))


# using 4 instead of 2 is useful for easily detecting wins (and when to block) using sum()
M = [4 if x==2 else x for x in start]


# the indices of locations that are still unfilled
spotsFree = [x for x in range(9) if start[x]==0]


# check start[] for obvious situations or moves
# sums[i] is the sum of indices[i] of M
sums = [sum([M[x] for x in indices[y]]) for y in range(8)]
if 3 in sums or 12 in sums:
  print("  looks like the game is over, right?")
  exit()
if 2 in sums or 8 in sums:
  print("  you don't really have much of a choice, do you?")
  exit()




# Recursive function to populate results[]
# This function returns...
#      2 for being able to force a win
#      1 for being able to win if opponent isn't the best
#      0 for pure draws
#     -1 for being opponent being able to force a loss
# These values go into results[] when step is 1
def analyzeMoves( M, spotsFree, step ):
  global results, counter

  # counter is for indexing results[]
  if step == 1:
    counter += 1

  if step & 1:   # if step is odd
    oppenentTurn = True    # note that step starts at 0
  else:
    oppenentTurn = False

  if len(spotsFree) & 1:  # if len(spotsFree) is odd
    newValue = 1    # place a 1 instead of a 4 on the tic-tac-toe board
    blockCondition = 8  # if, let's say, sum(row) is 8, block
  else:
    newValue = 4
    blockCondition = 2

  # sums[i] is the sum of indices[i] of M
  sums = [sum([M[x] for x in indices[y]]) for y in range(8)]
  if blockCondition in sums:   # block

      type = sums.index(blockCondition)
      ind = [x for x in indices[type] if M[x]==0][0]  # location to block

      M[ind] = newValue
      spotsFree.remove(ind)

      sums = [sum([M[x] for x in indices[y]]) for y in range(8)]
      if blockCondition in sums:  # win if there is another thing needing to be blocked!

          if oppenentTurn:
            v = 2  # won!
          else:
            v = -1  # lost

          if step == 1:
            results[counter] = v
          return v

      else:
          v = analyzeMoves( M, spotsFree, step+1 )
          if step == 1:
            results[counter] = v
          return v

  else:

      list = [None]*len(spotsFree)
      for i in range(len(spotsFree)):

          # I must make copies because you can't pass by value in Python
          M2 = M[:]
          spotsFree2 = spotsFree[:]

          ii = spotsFree[i]  #the index of the piece to be added on new board
          M2[ii] = newValue  #add piece to new board
          del spotsFree2[i]  #update the new list of available moves

          list[i] = analyzeMoves( M2, spotsFree2, step+1 )

      # process list[] to find v; that is, combine multiple outputs of analyzeMoves()
      if len(list)==0:

          v = 0   # draw

      elif oppenentTurn:
          
          if any(i==-1 for i in list):
            v = -1
          elif any(i==1 for i in list) or (any(i==0 for i in list) and any(i==2 for i in list)):
            v = 1
          else:
            v = list[0]    # either all of list[] is 2 or all of list is 0

      else:

          # choose the highest situation in the list
          v = max(list)

      # take care of results[] and return
      if step == 1:
        results[counter] = v
      return v




# do it!
results = [0]*len(spotsFree)
counter = -1
analyzeMoves( M, spotsFree[:], 0 )



# print results[]
for location, result in zip(spotsFree,results):

  if result==-1:
    print( '  location', location+1, 'will allow your opponent to force a win' )
  elif result==0:
    print( '  location', location+1, 'will lead to a draw' )
  elif result==1:
    print( '  location', location+1, 'might allow you to force a win' )
  elif result==2:
    print( '  location', location+1, 'will allow you to force a win' )


  elif all(l==1 or l==2 for l in list):
    string = 'has '
    if any(l==1 for l in list):
      string += 'losses '
    if any(l==2 for l in list):
      if len(string) > 4:
        string += 'and wins '
      else:
        string += 'wins '
    print( '  location', i+1, string + 'possible' )
  elif any(l==4 for l in list):
    print( '  location', i+1, 'will force a win' )
    if len(list) != 1:
      print('huh!')
  else:              # is it possible to have 3 and -1 or 0 ?
    if any(l==-1 for l in list):
      print( '  location', i+1, 'will allow your opponent to force a win with just one move' )
    elif any(l==0 for l in list):
      print( '  location', i+1, 'will allow your opponent to force a win' )
    if any(l==3 for l in list):
      print( '  location', i+1, 'will allow you to force a win' )

