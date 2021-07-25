#!/usr/bin/env python3.8
#
# Play Tic-tac-toe with the computer, but the computer will never let you win.
# Runs in a terminal (on Windows, the Command Prompt).
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
# Depending on how the Greedy variable is set, you will get different experiences...
#   Greedy = 0: computer prevents you from having the opportunity to force it to lose
#   Greedy = 1: computer will also avoid situations that satisfy
#               both that it can lose and that the human cannot win
#   Greedy = 2: computer will also avoid situations that are a draw
#   Greedy = 3: computer will always favor situations that guarantee that it can win
#
# If the computer is not avoiding a couple types of situations,
# to keep gameplay interesting,
# it will randomly choose between the allowed locations.
# If the computer is avoiding a couple types of situations,
# it will avoid the worse situation more.
#
# I suppose you could set Greedy to -1 to have the computer do more random moves,
# while still always completing any almost-complete line or blocking your
# almost-complete line.

Greedy = 0



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



# Returns...
#  -1 if other player can force a win with just one move 
#   0 if other player can force a win with multiple moves
#   1 if other player wins
#   2 if you win
#   3 if you can force a win in multiple moves
#   4 if you will force a win
# A player, in general, forces a win if all future moves lead to a win,
#   and I think the function below checks for all POSSIBLE instances of this.
#   That is, I don't think I need to compare different history[] lists.
def analyzeHistory(history):

  length = len(history)

  if length & 1:   # if length is odd, you won!
    if all(h==9 for h in history[1::2]):  # you can force a win
      if all(h==9 for h in history[2::2]):
        return 4
      return 3
    return 2
  else:
    if all(h==9 for h in history[2::2]):
      if all(h==9 for h in history[3::2]):
        return -1
      return 0
    return 1




# recursive function
def analyzeMoves( M, spotsFree, history ):
  global results

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
          results += [history[0], analyzeHistory(history)]
      else:
          analyzeMoves( M, spotsFree, history+[9] )  # 9 means block

  else:
      for i in range(len(spotsFree)):

          # I must make copies because you can't pass by value in Python
          M2 = M[:]
          spotsFree2 = spotsFree[:]

          ii = spotsFree[i]  #the index of the piece to be added on new board
          M2[ii] = newValue  #add piece to new board
          del spotsFree2[i]  #update the new list of available moves

          analyzeMoves( M2, spotsFree2, history+[ii] )



human = int(input("  Do you want to be player 1 or 2? "))

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



  # Grows as analyzeMoves() is recursively called
  # Values come in pairs: [a,a,b,b,c,c,...]
  results = []


  # do it!
  analyzeMoves( M, spotsFree[:], [] )


  # Analyze results[] to create resultsAnalyzed[] of length len(spotsFree),
  # where resultsAnalyzed corresponds to the Greedy level and goes from -1 to 3
  counter = 0
  resultsAnalyzed = [-1]*len(spotsFree)
  for j,i in enumerate(spotsFree):   # j is index; i is spotsFree[j]

    list = []
    while counter < len(results) and results[counter]==i:
      counter += 1
      list += [results[counter]]
      counter += 1

    if len(list)==0:
      resultsAnalyzed[j] = 1
    elif all(l==1 or l==2 for l in list):
      if all(l==1 for l in list):
        resultsAnalyzed[j] = 0
      else:
        resultsAnalyzed[j] = 2
    elif any(l==4 for l in list):
      resultsAnalyzed[j] = 3
      if len(list) != 1:
        print('huh!')
    elif any(l==-1 for l in list):
      resultsAnalyzed[j] = -1
    elif any(l==0 for l in list):
      resultsAnalyzed[j] = -1
    elif any(l==3 for l in list):
      resultsAnalyzed[j] = 3
    else:
      print('whoa!')


  # make the computer's move
  list = []
  cutoff = Greedy
  while len(list) == 0:
    list = [i for j,i in enumerate(spotsFree) if resultsAnalyzed[j] >= cutoff]
    cutoff -= 1
  ind = list[random.randint(0, len(list)-1)]
  M[ind] = computer
  myPrint(M)
  spotsFree.remove(ind)

  # check for draw
  if 0 not in M:
    print("  Draw!")
    break

