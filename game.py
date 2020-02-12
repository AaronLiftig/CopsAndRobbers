import numpy as np
import random

# Currently, the robber moves first,
# meaning that the robber, if 'random,' can lose by moving onto the cop.
# This avoids the players not acknowledging when they cross paths,
# though there are other ways to avoid this that are less 'turn-based.'

class createGame:
    def __init__(self):
        self.robName,self.copName = 1,2

def createMatrix(game):
    return np.zeros((game.m,game.n))

def printMatrix(game,iterCount):
    print('Iteration:',iterCount)
    print(game.matrix,'\n')
    pass # For when print statements are commented out.

def placeRob(game,place):
    # place is a location on an 0-indexed, mxn matrix
    # otherwise, enter an (m,n) tuple
    if place == 'random':
        m_pr = random.randint(0,game.m-1)
        n_pr = random.randint(0,game.n-1)
        game.matrix[m_pr][n_pr] = game.robName
        return [m_pr,n_pr]	
    elif place.__class__ == tuple:
        m_pr = place[0]
        n_pr = place[1]
        game.matrix[m_pr][n_pr] = game.robName
        return [m_pr,n_pr]

def robChar(game,howDrunk,robMove):
    game.robDrunk = howDrunk # Doesn't move this percent of the time
    game.robMove = robMove # Moves two squares this percent of the time

def placeCop(game,place): 
    # place is a location on a 0-indexed, mxn matrix that is not occupied by the robber
    # otherwise, enter an (m,n) tuple
    if place == 'random':
        m_pc = random.randint(0,game.m-1)
        n_pc = random.randint(0,game.n-1)
        if (m_pc != game.robPlace[0]) | (n_pc != game.robPlace[1]):
            game.matrix[m_pc][n_pc] = game.copName	
        else:
            [m_pc,n_pc] = placeCop(game,place=place)		
    elif place.__class__ == tuple:
        m_pc = place[0]
        n_pc = place[1]
        game.matrix[m_pc][n_pc] = game.copName
    return [m_pc,n_pc]

def copChar(game,howDrunk,copMove):
    game.copDrunk = howDrunk # Doesn't move this percent of the time
    game.copMove = copMove

def startChase(game,runTest):
    # TODO for robber on board (when multiple robbers spawn in)
    for turn in range(game.robMove):    
        purposeful = drunkFunc(game,'rob',runTest)
        if purposeful == True:
            directFunc(game,'rob') # Robber avoids cop
        else:
            randomMove(game,'rob',runTest) # Robber randomly moves 
        caught = checkIfCaught(game)
        if caught == True:
            return caught
    # TODO for cop on board (when multiple cops spawn in)
    for turn in range(game.copMove):
        purposeful = drunkFunc(game,'cop',runTest)
        if purposeful == True:  
            directFunc(game,'cop') # Cop chases robber        
        else: 
            randomMove(game,'cop',runTest) # Cop randomly moves
        caught = checkIfCaught(game)
        if caught == True:
            return caught  
    return caught

def drunkFunc(game,playerString,runTest):
    place,name,drunk = sidePick(game,playerString)
    purposeful = random.choices([False,True],[drunk,1-drunk])
    if runTest==False:
        print('Move:',playerString)
        print('purposeful:',purposeful[0])
        print('place:',place,'\n')
    return purposeful[0]

def sidePick(game,playerString):
    if playerString.lower() == 'rob':
        place = game.robPlace
        name = game.robName
        drunk = game.robDrunk
    elif playerString.lower() == 'cop':
        place = game.copPlace
        name = game.copName
        drunk = game.copDrunk
    return place,name,drunk

def randomMove(game,playerString,runTest): # Finds possible move for player
    place,name,drunk = sidePick(game,playerString)
    game.matrix[place[0]][place[1]] = 0 # Removes previous location
    
    if playerString == 'rob':
        move(game,game.robPlace,game.robName,game.oneMoveList,runTest)   
    elif playerString == 'cop':
        move(game,game.copPlace,game.copName,game.oneMoveList,runTest)

def move(game,place,name,choices,runTest):
    moveTup = random.choice(choices)
    place[0] = (place[0] + moveTup[0]) % game.m
    place[1] = (place[1] + moveTup[1]) % game.n 
    if runTest==False:
        print('Up/Down:',moveTup[0],'to',place[0])  
        print('Side/Side:',moveTup[1],'to',place[1],'\n')
    game.matrix[place[0]][place[1]] = name 

def directFunc(game,playerString): # Cop chase robber and/or robber avoids cop.
    place,name,drunk = sidePick(game,playerString)
    robPlace = game.robPlace
    copPlace = game.copPlace
    game.matrix[place[0]][place[1]] = 0 # Removes robber/cop's previous location
    #vertical
    if (robPlace[0]-copPlace[0])%game.m > (copPlace[0]-robPlace[0])%game.m:
        place[0] = (place[0]-1)%game.m # Player moves up
    elif (robPlace[0]-copPlace[0])%game.m < (copPlace[0]-robPlace[0])%game.m:
        place[0] = (place[0]+1)%game.m # Player moves down
    elif (robPlace[0]-copPlace[0])%game.m == 0: # Catches where cop and robber are on same row
        if playerString == 'rob':
            place[0] = (place[0]-1)%game.m # Robber moves up, but cop stays
    elif (robPlace[0]-copPlace[0])%game.m == (copPlace[0]-robPlace[0])%game.m:
        if playerString == 'cop':
            place[0] = (place[0]-1)%game.m # Cop moves up, but robber stays
    #horizontal
    if (robPlace[1]-copPlace[1])%game.n > (copPlace[1]-robPlace[1])%game.n:
        place[1] = (place[1]-1)%game.n
        game.matrix[place[0]][place[1]] = name # Player moves left
    elif (robPlace[1]-copPlace[1])%game.n < (copPlace[1]-robPlace[1])%game.n:
        place[1] = (place[1]+1)%game.n
        game.matrix[place[0]][place[1]] = name # Player moves right
    elif (robPlace[1]-copPlace[1])%game.n == 0: # Catches where cop and robber are on same column
        if playerString == 'rob':
            place[1] = (place[1]-1)%game.m # Robber moves left, but cop stays
        game.matrix[place[0]][place[1]] = name
    elif (robPlace[1]-copPlace[1])%game.n == (copPlace[1]-robPlace[1])%game.n:
        if playerString == 'cop':
            place[1] = (place[1]-1)%game.n
        game.matrix[place[0]][place[1]] = name # Cop moves left, but robber stays

def checkIfCaught(game):
    if game.robPlace != game.copPlace:
        game.matrix[game.copPlace[0]][game.copPlace[1]] = game.copName
        return False
    elif game.robPlace == game.copPlace:
        game.matrix[game.robPlace[0]][game.robPlace[1]] = 3
        return True

def Again():
    playAgain = input('Play again? Enter y or n.')
    if playAgain.lower() == 'n':
        exit() 
    elif playAgain.lower() == 'y':
        return
    else:
        Again()

def playGame(robDrunk=.5,copDrunk=.5,robMove=1,copMove=1,robPlace='random',copPlace='random',runTest=False,iterNumber=50):
    oneMoveList = [(a,b) for a in range(-1,2) for b in range(-1,2)] # By default, can move diagonally and stand still
    # for x in [(0,0),(-1,1),(-1,-1),(1,-1),(1,1)]:
    #     oneMoveList.remove(x) # Vertical and horizontal only
    
    testCount = 0
    testList = []
    
    x = int(input('Enter number of rows:'))
    y = int(input('Enter number of columns:'))

    while True:
        game = createGame()
        game.oneMoveList = oneMoveList
        
        game.m = x
        game.n = y
        iterCount = 0
        game.matrix = createMatrix(game)

        game.robPlace = placeRob(game,robPlace)
        robChar(game,robDrunk,robMove)
        game.copPlace = placeCop(game,copPlace)
        copChar(game,copDrunk,copMove)

        if runTest==False:
            printMatrix(game,iterCount)
            print('Locations:\n','robber:',game.robPlace,'cop:',game.copPlace,'\n'*2)

        while True:
            caught = startChase(game,runTest)
            iterCount += 1

            if runTest==False:
                printMatrix(game,iterCount)
                print('Locations:\n','robber:',game.robPlace,'cop:',game.copPlace,'\n'*3)
            
            if caught == True:
                break

        if runTest==False:
            print('The cop caught the robber.')
            print('It took '+ str(iterCount) +' iterations.')
      
        # If runTest=True, don't comment out print statements below this point.
        if runTest == True:
            if testCount != iterNumber:
                testList.append(iterCount)
                testCount += 1
            else:
                print('Over',iterNumber,'iterations,')
                print('the average iteration was', np.mean(testList))
                print('List of iterations during test:\n',testList)
                Again()
                testCount = 0
                testList = []
        else:
            Again()

playGame(robDrunk=.5,copDrunk=0,robMove=2,copMove=1,robPlace='random',copPlace='random',runTest=True,iterNumber=50)

# robDrunk and copDrunk are the probability that the respective players move randomly

# robMove and copMove represent the number of moves the robber and cop are given each turn

# To manually place robber and cop, change robPlace and/or copPlace from 'random',
# to tuples representing one or both's placement on a 0-indexed, mxn matrix.

# If you would like to calculate the average of a certain number of cycles, 
# change runtest to True and adjust the iterNumber accordingly.
# Print statments have been made conditional on the runTest variable in order to have a manageable output screen.
