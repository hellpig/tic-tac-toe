#!/usr/bin/env python3.8
#
# Play Tic-tac-toe with the computer, but the computer will never let you win.
# Runs in a terminal (on Windows, PowerShell or the Command Prompt).
#
# The numbers for the locations are...
#    1 2 3
#    4 5 6
#    7 8 9
# Note that these are temporarily 0-8 (not 1-9) in the code.
#
# The computer will try to win whenever there is 2 of its own in a line.
# The computer will always block whenever there are 2 of yours in a line
# Winning takes priority over blocking!

# Internally using 4 instead of 2 is useful for easily detecting wins
#   (and when to block) using sum()


# My goal is to make the experience as interesting as possible,
# so the computer will not necessarily greedily try to win.
# That is, the computer will not necessarily keep trying the best moves each game.
# Depending on how the Greediness variable is set, you will get different experiences...
#   Greediness = 0: computer prevents you from having the opportunity to force it to lose
#   Greediness = 1: computer will also avoid situations that are a draw
#   Greediness = 2: computer will always favor situations that guarantee that it can win
#
# If the computer is not avoiding a couple types of situations,
# to keep gameplay interesting,
# it will randomly choose between the allowed locations.
# If the computer is avoiding a couple types of situations,
# it will avoid the worse situation more.
#
# I suppose you could set Greediness to -1 to have the computer do even more random moves,
# while still always completing any almost-complete line or blocking your
# almost-complete line.

Greediness = 0



import random



# 8 rows of this are for the...
#          first 3 columns,           then the first 3 rows,     then the 2 diagonals
indices = ((0,3,6), (1,4,7), (2,5,8), (0,1,2), (3,4,5), (6,7,8), (0,4,8), (6,4,2))



# print list as tic-tac-toe table
def myPrint(list):

  M = [2 if x==4 else x for x in list]

  print('')
  print('    ', M[0:3])
  print('    ', M[3:6])
  print('    ', M[6:9])
  print('\n')






# Recursive function to populate results[]
# This function returns...
#      2 for being able to force a win
#      1 for being able to win if opponent isn't the best
#      0 for pure draws
#     -1 for opponent being able to force a loss
# These values go into results[] when depth is 1
def analyzeMoves( M, spotsFree, depth ):
    global results, counter

    if depth & 1:   # if depth is odd
      oppenentTurn = True    # note that depth starts at 0
    else:
      oppenentTurn = False

    # counter is for indexing results[]
    if depth == 1:
      counter += 1

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

        if blockCondition in sums:  # win or lose if there is another thing needing to be blocked!

            if oppenentTurn:
              v = 2  # won!
            else:
              v = -1  # lost

            if depth == 1:
              results[counter] = v
            return v

        else:
            v = analyzeMoves( M, spotsFree, depth+1 )
            if depth == 1:
              results[counter] = v
            return v

    else:

        # call analyzeMoves() for each possible next move and create list[]
        list = [0]*len(spotsFree)
        for i in range(len(spotsFree)):

            # I must make copies because you can't pass by value in Python
            M2 = M[:]
            spotsFree2 = spotsFree[:]

            ii = spotsFree[i]  #the index of the piece to be added on new board
            M2[ii] = newValue  #add piece to new board
            del spotsFree2[i]  #update the new list of available moves

            list[i] = analyzeMoves( M2, spotsFree2, depth+1 )

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
        if depth == 1:
          results[counter] = v
        return v



human = int(input("  Do you want to be player 1 or 2? Enter 1 or 2: "))

if human!=1 and human!=2:
  print("  error: choose 1 or 2")
  exit()

# computer and human will be either 1 and 4 or 4 and 1
computer = 1
if human==1:
  computer = 4
  blockCond = 2
if human==2:
  human = 4
  blockCond = 8


# initialize the board to zeros
M = [0]*9


# let the computer go first if it is supposed to
if human == 4:
  # randomly choose between center, corner, and side
  v = random.randint(1,3)
  if v==1:   # center
    M[4] = 1
  elif v==2:  # corner
    M[ [0,2,6,8][random.randint(0,3)] ] = 1
  else:      # side
    M[ [1,3,5,7][random.randint(0,3)] ] = 1

# the indices of locations that are still unfilled
spotsFree = [x for x in range(9) if M[x]==0]

myPrint(M)



# each iteration is a move by human then computer
while True:

  # check for draw
  if 0 not in M:
    print("  Draw!")
    break

  while True:
    ind = int(input("  Make your move (enter 1-9): ")) - 1

    if ind in spotsFree:
      break

    print("    invalid move!")


  M[ind] = human
  myPrint(M)
  spotsFree.remove(ind)

  # sums[i] is the sum of indices[i] of M
  sums = [sum([M[x] for x in indices[y]]) for y in range(8)]

  # check for win
  if 3 in sums or 12 in sums:
    print("  Whahuh!?!?!?! You win!")
    break

  # check for draw
  if 0 not in M:
    print("  Draw!")
    break

  # check to see if computer will win
  if (computer == 1 and 2 in sums) or (computer == 4 and 8 in sums):
    print("  Computer would beat you in its next move!")
    break






  # if computer must block, block and continue
  number = len([i for i in sums if i==blockCond])
  if number:
    which = random.randint(1,number)

    for i in range(which):
      type = sums.index(blockCond)
      sums[type] = 0

    ind = [x for x in indices[type] if M[x]==0][0]  # location to block

    M[ind] = computer
    myPrint(M)
    spotsFree.remove(ind)

    continue



  # analyze puzzle to create results[]
  results = [0]*len(spotsFree)
  counter = -1
  analyzeMoves( M, spotsFree[:], 0 )
  #print(results)


  # make the computer's move
  list = []
  cutoff = Greediness
  while len(list) == 0:
    list = [i for j,i in enumerate(spotsFree) if results[j] >= cutoff]
    cutoff -= 1
  ind = list[random.randint(0, len(list)-1)]
  M[ind] = computer
  myPrint(M)
  spotsFree.remove(ind)


