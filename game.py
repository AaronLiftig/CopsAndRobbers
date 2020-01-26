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

def robChar(game,howDrunk,escape,rob2Move):
    game.robDrunk = howDrunk # Doesn't move this percent of the time
    game.robEscape = escape # If true, it tries to avoid cop
    game.rob2Move = rob2Move # Moves two squares this percent of the time

def placeCop(game,place): 
    # place is a location on a 0-indexed, mxn matrix that is not occupied by the robber
    # otherwise, enter an (m,n) tuple
    if place == 'random':
        m_pc = random.randint(0,game.m-1)
        n_pc = random.randint(0,game.n-1)
        if (m_pc != game.robPlace[0]) | (n_pc != game.robPlace[1]):
            game.matrix[m_pc][n_pc] = game.copName
            return [m_pc,n_pc]	
        else:
            [m_pc,n_pc] = placeCop(game,place=place)		
    elif place.__class__ == tuple:
        m_pc = place[0]
        n_pc = place[1]
        game.matrix[m_pc][n_pc] = game.copName
        return [m_pc,n_pc]

def copChar(game,howDrunk,chase):
    game.copDrunk = howDrunk # Doesn't move this percent of the time
    game.copChase = chase # If true, it tries to catch robber

def startChase(game):
    go = drunkFunc(game,'rob')
    if go == True:
        if game.robEscape == False: # Robber randomly moves
            randomMove(game,'rob')
        else: # Robber avoids cop
            directFunc(game,'rob')
        caught = checkIfCaught(game)
        if caught == True:
            return caught
    
    go = drunkFunc(game,'cop')
    if go == True:  
        if game.copChase == True: # Cop chases robber
            directFunc(game,'cop')
        else: # Cop randomly moves
            randomMove(game,'cop')
        caught = checkIfCaught(game)
        return caught
    else:
        return False

def drunkFunc(game,playerString):
    print('Move:',playerString)
    place,name,drunk = sidePick(game,playerString)
    go = random.choices([False,True],[drunk,1-drunk])
    print('Go:',go[0])
    print('place:',place,'\n')
    return go[0]

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

def randomMove(game,playerString): #Finds possible move for player
    place,name,drunk = sidePick(game,playerString)
    game.matrix[place[0]][place[1]] = 0 # Removes previous location
    
    if playerString == 'rob':
        if game.rob2Move == False:
            move(game,game.robPlace,game.robName,game.oneMoveList)
        elif game.rob2Move == True:
            move(game,game.robPlace,game.robName,game.twoMoveList)
    elif playerString == 'cop':
        move(game,game.copPlace,game.copName,game.oneMoveList)

def move(game,place,name,choices):
    moveTup = random.choice(choices)
    
    place[0] = (place[0] + moveTup[0]) % game.m
    print('Up/Down:',moveTup[0],'to',place[0]) 
    
    place[1] = (place[1] + moveTup[1]) % game.n  
    print('Side/Side:',moveTup[1],'to',place[1],'\n')
    
    game.matrix[place[0]][place[1]] = name 

def directFunc(game,playerString): # Cop chase robber and/or robber avoids cop.
    place,name,drunk = sidePick(game,playerString)
    robPlace = game.robPlace
    copPlace = game.copPlace
    
    game.matrix[place[0]][place[1]] = 0 # Removes players' previous location
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

def playGame(robDrunk=.5,copDrunk=.5,robEscape=False,copChase=True,rob2Move=False,robPlace='random',copPlace='random'):
    oneMoveList = [(a,b) for a in range(-1,2) for b in range(-1,2)]
    oneMoveList.remove((0,0))
    twoMoveList = [(a,b) for a in range(-2,3) for b in range(-2,3)]
    twoMoveList.remove((0,0))
    
    while True:
        game = createGame()
        game.oneMoveList = oneMoveList
        game.twoMoveList = twoMoveList
        
        game.m = int(input('Enter number of rows:'))
        game.n = int(input('Enter number of columns:'))
        iterCount = 0
        game.matrix = createMatrix(game)

        game.robPlace = placeRob(game,robPlace)
        robChar(game,robDrunk,robEscape,rob2Move)
        game.copPlace = placeCop(game,copPlace)
        copChar(game,copDrunk,copChase)

        printMatrix(game,iterCount)
        print('Locations:\n','robber:',game.robPlace,'cop:',game.copPlace,'\n'*2)

        while True:
            caught = startChase(game)
            iterCount += 1

            printMatrix(game,iterCount)
            print('Locations:\n','robber:',game.robPlace,'cop:',game.copPlace,'\n'*3)
            
            if caught == True:
                break

        print('The cop caught the robber.')
        print('It took '+ str(iterCount) +' iterations.')

        playAgain = input('Play again? Enter y or n.')
        if playAgain == 'n':
            exit()


playGame(robDrunk=.5,copDrunk=.5,robEscape=True,copChase=True,rob2Move=False,robPlace='random',copPlace='random')

# robDrunk and copDrunk are the probability that the respective players DON'T move
# robEscape and copChase are whether the rob avoids and the cop follows. 'False' means random movement for that player.
# rob2Move being 'True' means that the robber has a chance to move 1 or 2 spaces on the turns where they do move.
# placeRob and placeCop are not 'random', input tuples representing one or both's placement on a 0-indexed, mxn matrix.
