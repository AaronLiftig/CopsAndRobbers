import numpy as np
import random

def createMatrix(m,n):
	return np.zeros((m,n))

def placeRob(m,n,matrix,place='random'):
	# place is a location on an mxn matrix
	# otherwise, enter an (m,n) tuple
	if place == 'random':
		m_pr = random.randint(0,m-1)
		n_pr = random.randint(0,n-1)
		matrix[m_pr][n_pr] = 1
		return m_pr,n_pr	
	elif place.__class__ == tuple:
		m_pr = place[0]
		n_pr = place[1]
		matrix[m_pr][n_pr] = 1
		return m_pr,n_pr

def robChar(rob,howDrunk=.5,escape=False,twoMoveProb=0):
	rob.drunk = howDrunk
	rob.escape = escape
	rob.twomove = twoMoveProb
	return rob

def placeCop(m_pr,n_pr,m,n,matrix,place='random'): 
	# place is a location on an mxn matrix that is not occupied by the robber
	# otherwise, enter an (m,n) tuple
	if place == 'random':
		m_pc = random.randint(0,m-1)
		n_pc = random.randint(0,n-1)
		if (m_pc != m_pr) | (n_pc != n_pr):
			matrix[m_pc][n_pc] = 2
		else:
			placeCop(m_pr,n_pr,m,n,matrix,place=place)
	elif place.__class__ == tuple:
		m_pc = place[0]
		n_pc = place[1]
		matrix[m_pc][n_pc] = 2

def copChar(cop,howDrunk=.5,chase=True):
	cop.drunk = howDrunk
	cop.chase = chase
	return cop

def startChase():
	robMove()
	copMove()
	pass

def playGame():
	m = int(input('Enter number of rows:'))
	n = int(input('Enter number of columns:'))
	iterCount = 0

	matrix = createMatrix(m,n)
	rob,cop = object,object
	
	m_pr,n_pr = placeRob(m,n,matrix)
	rob = robChar(rob)
	placeCop(m_pr,n_pr,m,n,matrix)
	cop = copChar(cop)

	print('\n','Iteration:',iterCount)
	print(matrix,'\n')

	while rob.locate != cop.locate:
		startChase()



playGame()
