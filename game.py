import numpy as np
import random

# Currently, the robber moves first,
# meaning that the robber can lose by moving onto the cop.
# This avoids the players not acknowledging when they cross paths,
# Though there are other ways to avoid this that are less 'turn-based.'

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

def robChar(game,howDrunk,escape,twoMoveProb):
    game.robDrunk = howDrunk # Doesn't move this percent of the time
    game.robEscape = escape # If true, it tries to avoid cop
    game.robTwoMove = twoMoveProb # Moves two squares this percent of the time
    return game

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
    return game

def startChase(game):
    go = drunkFunc(game,'rob')
    if go == True:
        if game.robEscape == False: # Robber randomly moves
            game = randomMove(game,'rob')
        else: # Robber avoids cop
            game = directFunc(game,'rob')
        caught,game = checkIfCaught(game)
        if caught == True:
            return caught,game
    
    go = drunkFunc(game,'cop')
    if go == True:  
        if game.copChase == True: # Cop chases robber
            game = directFunc(game,'cop')
        else: # Cop randomly moves
            game = randomMove(game,'cop')
        caught,game = checkIfCaught(game)
        return caught,game
    else:
        return False, game

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
    oldVert = place[0] # Stores previous location to check if player moved vertically
    game = vertMove(game,place,name,[-1,0,1])
    if oldVert == place[0]: # Must move horizontally if not vertically
        game = horizMove(game,place,name,[-1,1])
    else:
        game = horizMove(game,place,name,[-1,0,1])
    return game

def vertMove(game,place,name,choices):
    vert = random.choice(choices)
    place[0] += vert
    place[0] %= game.m
    print('Up/Down:',vert,'to',place[0])
    return game

def horizMove(game,place,name,choices):
    horiz = random.choice(choices)
    place[1] += horiz 
    place[1] %= game.n   
    game.matrix[place[0]][place[1]] = name
    print('Side/Side:',horiz,'to',place[1],'\n')
    return game

def directFunc(game,playerString): # Has cop chase robber
    place,name,drunk = sidePick(game,playerString)
    robPlace = game.robPlace
    copPlace = game.copPlace
    
    game.matrix[place[0]][place[1]] = 0 # Removes cop's previous location
    #vertical
    if (robPlace[0]-copPlace[0])%game.m > (copPlace[0]-robPlace[0])%game.m:
        place[0] = (place[0]-1)%game.m # Cop moves up
    elif (robPlace[0]-copPlace[0])%game.m < (copPlace[0]-robPlace[0])%game.m:
        place[0] = (place[0]+1)%game.m # Cop moves down
    elif (robPlace[0]-copPlace[0])%game.m == 0: # Catches where cop and robber are on same row
        pass
    elif (robPlace[0]-copPlace[0])%game.m == (copPlace[0]-robPlace[0])%game.m:
        place[0] = (place[0]-1)%game.m # Breaks stalemate by choosing up
    #horizontal
    if (robPlace[1]-copPlace[1])%game.n > (copPlace[1]-robPlace[1])%game.n:
        game.matrix[place[0]][(place[1]-1)%game.n] = name # Cop moves left
        place[1] = (place[1]-1)%game.n
    elif (robPlace[1]-copPlace[1])%game.n < (copPlace[1]-robPlace[1])%game.n:
        game.matrix[place[0]][(place[1]+1)%game.n] = name # Cop moves right
        place[1] = (place[1]+1)%game.n
    elif (robPlace[1]-copPlace[1])%game.n == 0: # Catches where cop and robber are on same row
        game.matrix[place[0]][place[1]] = name # Horizontal stay same
    elif (robPlace[1]-copPlace[1])%game.n == (copPlace[1]-robPlace[1])%game.n:
        game.matrix[place[0]][(place[1]-1)%game.n] = name # Breaks stalemate by choosing left
        place[1] = (place[1]-1)%game.n
    return game

def checkIfCaught(game):
    if game.robPlace != game.copPlace:
        game.matrix[game.copPlace[0]][game.copPlace[1]] = game.copName
        return False,game
    elif game.robPlace == game.copPlace:
        game.matrix[game.robPlace[0]][game.robPlace[1]] = 3
        return True,game

def playGame(robDrunk=.5,copDrunk=.5,robEscape=False,copChase=True,rob2MoveProb=0,robPlace='random',copPlace='random'):
    while True:
        game = createGame()
        
        game.m = int(input('Enter number of rows:'))
        game.n = int(input('Enter number of columns:'))
        iterCount = 0
        game.matrix = createMatrix(game)

        game.robPlace = placeRob(game,robPlace)
        game = robChar(game,robDrunk,robEscape,rob2MoveProb)
        game.copPlace = placeCop(game,copPlace)
        game = copChar(game,copDrunk,copChase)

        printMatrix(game,iterCount)
        print('Locations:\n','robber:',game.robPlace,'cop:',game.copPlace,'\n'*2)

        while True:
            caught,game = startChase(game)
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

playGame(robDrunk=.5,copDrunk=.5,robEscape=True,copChase=True,rob2MoveProb=0,robPlace='random',copPlace='random')
# placeRob and placeCop are tuples representing placement on a 0-indexed, mxn matrix.
# Chasing has been implemented for the cop.
# TODO Still need to implement escape, 2-jump move by robber, and fix matrix bugs.
