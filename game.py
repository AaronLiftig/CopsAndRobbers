import numpy as np
import random

class createGame:
	def __init__(self):
		self.robName,self.copName = 1,2

def createMatrix(game):
	return np.zeros((game.m,game.n))

def placeRob(game,place='random'):
	# place is a location on an mxn matrix
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
		
def robChar(game,howDrunk=.5,escape=False,twoMoveProb=0):
	game.robDrunk = howDrunk # Doesn't move this percent of the time
	game.robEscape = escape # If true, it tries to avoid cop
	game.robTwoMove = twoMoveProb # Moves two squares this percent of the time
	return game

def placeCop(game,place='random'): 
	# place is a location on an mxn matrix that is not occupied by the robber
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

def copChar(game,howDrunk=.5,chase=True):
	game.copDrunk = howDrunk # Doesn't move this percent of the time
	game.copChase = chase # If true, it tries to catch robber
	return game

def printMatrix(game,iterCount):
	print('\n','Iteration:',iterCount)
	print(game.matrix,'\n')

def startChase(game):
	game = move(game,'rob')
	caught,game = checkIfCaught(game)
	if caught == True:
		return caught,game
	game = move(game,'cop')
	caught,game = checkIfCaught(game)
	return caught,game

def move(game,playerString): #Finds possible move for player
	place,name,drunk = sidePick(game,playerString)
	go = random.choices([False,True],[drunk,1-drunk])
	print('go:',go)
	if go[0] == True:
		game.matrix[place[0]][place[1]] = 0
		oldVert = place[0]
		game = vertMove(game,place,name,[-1,0,1])
		if oldVert == place[0]: # Must move horizontally if not vertically
			game = horizMove(game,place,name,[-1,1])
		else:
			game = horizMove(game,place,name,[-1,0,1])
		print('Move:',vertMove,horizMove)
	return game

def checkIfCaught(game):
	if game.robPlace == game.copPlace:
		game.matrix[game.robPlace[0]][game.robPlace[1]] = 3
		return True,game
	elif game.robPlace != game.copPlace:
		game = placeOnMatrix(game,game.copPlace,game.copName)
		return False,game

def placeOnMatrix(game,place,name):
	game.matrix[place[0]][place[1]] = name
	return game

def vertMove(game,place,name,choices):
	vert = random.choice(choices)
	try:
		game.matrix[place[0]+vert][place[1]] = name
		place[0] += vert
	except:
		pass		
	game = vertMove(game,place,name,choices)
	return game

def horizMove(game,place,name,choices):
	horiz = random.choice(choices)
	try:
		game.matrix[place[0]][place[1]+horiz] = name
		place[1] += horiz
	except:
		pass
	game = horizMove(game,place,choices)
	return game

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

def playGame():
	game = createGame()
	
	game.m = int(input('Enter number of rows:'))
	game.n = int(input('Enter number of columns:'))
	iterCount = 0
	game.matrix = createMatrix(game)

	game.robPlace = placeRob(game)
	game = robChar(game)
	game.copPlace = placeCop(game)
	game = copChar(game)

	printMatrix(game,iterCount)
	print(game.robPlace,game.copPlace)

	while True:
		caught,game = startChase(game)
		iterCount += 1

		printMatrix(game,iterCount)
		print(game.robPlace,game.copPlace)
		exit()
		if caught == True:
			break

	print('The cop caught the robber.')
	print('It took '+iterCount+' iterations.')


playGame()
