import numpy as np
import random

class DrunkenCopsAndRobbers:
    def __init__(self,robber_drunk_percentage=.5,
                cop_drunk_percentage=.5,
                robber_possible_turns=1,cop_possible_turns=1,
                robber_move_length=1,cop_move_length=1,
                can_move_diagonal=True,can_pass_turn=True,
                ply_before_new_robber_spawns=-1,
                robber_location='random',
                cop_location='random',
                run_multiple=False,number_of_games=50,
                max_game_iterations=1000):

        run_count = 0
        results_list = []

        self.robber_name,self.cop_name = 1,2
        self.robber_move_list,self.cop_move_list = [],[]

        self.get_move_list(robber_move_length,self.robber_move_list,
                            can_move_diagonal,can_pass_turn)
        self.get_move_list(cop_move_length,self.cop_move_list,
                            can_move_diagonal,can_pass_turn)

        self.m,self.n = 0,0
        self.get_matrix_dimensions()

        while True:
            iteration_count = 0
            self.matrix = self.create_matrix()

            self.placement_list = []
            if (robber_location == 'random' or \
                cop_location == 'random'):
                self.fill_placement_list()

            self.robber_location = \
                self.place(robber_location,self.robber_name)
            self.robber_attributes(robber_drunk_percentage,
                                    robber_move_length,
                                    robber_possible_turns)
            self.cop_location = \
                self.place(cop_location,self.cop_name)
            self.cop_attributes(cop_drunk_percentage,cop_move_length,
                                cop_possible_turns)

            if not run_multiple:
                self.print_matrix(iteration_count)
                print('Locations:\n','robber:',
                        self.robber_location,'cop:',
                        self.cop_location,'\n'*2)

            while True:
                caught = self.start_chase(run_multiple)
                iteration_count += 1

                if not run_multiple:
                    self.print_matrix(iteration_count)
                    print('Locations:\n','robber:',
                        self.robber_location,
                        'cop:',self.cop_location,'\n'*3)
                
                if (caught == True 
                    or iteration_count == max_game_iterations):
                    break

            if (iteration_count == max_game_iterations 
                and not run_multiple):
                print('The game reached the max_iteration_count')
            elif not run_multiple:
                print('The cop caught the robber.')
                print('It took '+ str(iteration_count) +' iterations.')
        
            # If run_multiple=True, don't comment out print statements
            # below this point.
            if run_multiple == True:
                if run_count != number_of_games:
                    results_list.append(iteration_count)
                    run_count += 1
                else:
                    print('Over',number_of_games,'games,')
                    print('the average iteration was',
                            np.mean(results_list))
                    print('List of iterations during test:\n',
                            results_list)
                    self.again()
                    run_count = 0
                    results_list = []
            else:
                self.again()

    def create_matrix(self):
        return np.zeros((self.m,self.n))

    def get_matrix_dimensions(self):
        while not self.m:
            try:
                self.m = abs(int(input('Enter number of rows:')))
            except:
                pass
        while not self.n:
            try:
                self.n = abs(int(input('Enter number of columns:')))
            except:
                pass

    def get_move_list(self,move_length,move_list,can_move_diagonal,
                        can_pass_turn):
        for a in range(-move_length,move_length+1):
            for b in range(-move_length,move_length+1):
                move_list.append((a,b))
        
        if not can_move_diagonal: # Vertical and horizontal only
            for i in range(1,move_length+1):
                move_list.remove((i,i))
                move_list.remove((i,-i))
                move_list.remove((-i,i))
                move_list.remove((-i,-i))

        if not can_pass_turn:
            move_list.remove((0,0))

    def fill_placement_list(self):
        for a in range(self.m):
            for b in range(self.n):
                self.placement_list.append((a,b))

    def print_matrix(self,iteration_count):
        print('Iteration:',iteration_count)
        print(self.matrix,'\n')

    def place(self,placement_tuple,name):
        # place is a location on an 0-indexed, mxn matrix
        # otherwise, enter an (m,n) tuple
        if placement_tuple == 'random':
            location = random.choice(self.placement_list)
            self.placement_list.remove(location)
            m,n = location[0],location[1]
            self.matrix[m][n] = name
            return [m,n]	
        elif (placement_tuple.__class__ == tuple 
            and len(placement_tuple) == 2 
            and list(map(type,placement_tuple)) == [int,int] 
            and 0 <= placement_tuple[0] <= self.m
            and 0 <= placement_tuple[1] <= self.n):
            
            m = placement_tuple[0]
            n = placement_tuple[1]
            self.matrix[m][n] = name
            return [m,n]
        else:
            print('placement_location must be "random" or an '
                + 'integer tuple within the grid')
            exit()

    def robber_attributes(self,drunk_percentage,robber_move_length,
                            robber_possible_turns):
        self.robber_drunk_percentage = drunk_percentage
        self.robber_move_length = robber_move_length
        self.robber_possible_turns = robber_possible_turns

    def cop_attributes(self,drunk_percentage,cop_move_length,
                        cop_possible_turns):
        self.cop_drunk_percentage = drunk_percentage
        self.cop_move_length = cop_move_length
        self.cop_possible_turns = cop_possible_turns

    def start_chase(self,run_multiple):
        # TODO for robber on board (when multiple robbers spawn in)
        for turn in range(self.robber_possible_turns):    
            purposeful = self.get_drunkenness('rob',run_multiple)
            if purposeful == True:
                self.get_direction('rob') # Robber avoids cop
            else:
                self.make_random_move('rob',run_multiple) 
                # Robber randomly moves 
            caught = self.check_if_caught()
            if caught == True:
                return caught
        # TODO for cop on board (when multiple cops spawn in)
        for turn in range(self.cop_possible_turns):
            purposeful = self.get_drunkenness('cop',run_multiple)
            if purposeful == True:  
                self.get_direction('cop') # Cop chases robber        
            else: 
                self.make_random_move('cop',run_multiple) 
                # Cop randomly moves
            caught = self.check_if_caught()
            if caught == True:
                return caught  
        return caught

    def get_drunkenness(self,player_string,run_multiple):
        place,name,drunk = self.get_side(player_string)
        purposeful = random.choices([False,True],[drunk,1-drunk])
        if not run_multiple:
            print('Move:',player_string)
            print('purposeful:',purposeful[0])
            print('place:',place,'\n')
        return purposeful[0]

    def get_side(self,player_string):
        if player_string.lower() == 'rob':
            place = self.robber_location
            name = self.robber_name
            drunk = self.robber_drunk_percentage
        elif player_string.lower() == 'cop':
            place = self.cop_location
            name = self.cop_name
            drunk = self.cop_drunk_percentage
        return place,name,drunk

    def make_random_move(self,player_string,run_multiple): 
    # Finds possible move for player
        place,name,drunk = self.get_side(player_string)
        self.matrix[place[0]][place[1]] = 0 # Removes previous location
        
        if player_string == 'rob':
            self.move(self.robber_location,self.robber_name,
                        self.robber_move_list,run_multiple)   
        elif player_string == 'cop':
            self.move(self.cop_location,self.cop_name,
                        self.one_move_list,run_multiple)

    def move(self,place,name,choices,run_multiple):
        # Replace position
        self.placement_list.append((place[0],place[1])) 
        move_tuple = random.choice(choices)
        place[0] = (place[0] + move_tuple[0]) % self.m
        place[1] = (place[1] + move_tuple[1]) % self.n 
        if not run_multiple:
            print('Up/Down:',move_tuple[0],'to',place[0])  
            print('Side/Side:',move_tuple[1],'to',place[1],'\n')
        # Remove new position
        self.placement_list.remove((place[0],place[1])) 
        self.matrix[place[0]][place[1]] = name 

    def get_direction(self,player_string): 
    # Cop chase robber and/or robber avoids cop.
        place,name,drunk = self.get_side(player_string)
        robber_location = self.robber_location
        cop_location = self.cop_location
        self.matrix[place[0]][place[1]] = 0 
        # Removes robber/cop's previous location
        #vertical
        if ((robber_location[0]
                - cop_location[0]) % self.m 
            > (cop_location[0]
                - robber_location[0]) % self.m):
            
            place[0] = (place[0] - 1) % self.m # Player moves up
        elif ((robber_location[0]
                - cop_location[0]) % self.m 
            < (cop_location[0] 
                - robber_location[0]) % self.m):
            
            place[0] = (place[0] + 1) % self.m # Player moves down
        elif (robber_location[0]
                - cop_location[0]) % self.m == 0: 
            # Catches where cop and robber are on same row
            if player_string == 'rob':
                place[0] = (place[0] - 1) % self.m 
                # Robber moves up, but cop stays
        elif ((robber_location[0]
                - cop_location[0]) % self.m 
            == (cop_location[0] 
                - robber_location[0]) % self.m):
            if player_string == 'cop':
                place[0] = (place[0] - 1) % self.m 
                # Cop moves up, but robber stays
        #horizontal
        if ((robber_location[1]
                - cop_location[1]) % self.n 
            > (cop_location[1]
                - robber_location[1]) % self.n):
            place[1] = (place[1] - 1) % self.n
            self.matrix[place[0]][place[1]] = name # Player moves left
        elif ((robber_location[1] 
                - cop_location[1])%self.n 
            < (cop_location[1]
                - robber_location[1]) % self.n):
            place[1] = (place[1]+1)%self.n
            self.matrix[place[0]][place[1]] = name # Player moves right
        elif (robber_location[1] 
            - cop_location[1]) % self.n == 0: 
            # Catches where cop and robber are on same column
            if player_string == 'rob':
                place[1] = (place[1] - 1) % self.m 
                # Robber moves left, but cop stays
            self.matrix[place[0]][place[1]] = name
        elif ((robber_location[1] 
                - cop_location[1]) % self.n 
            == (cop_location[1]
                - robber_location[1]) % self.n):
            if player_string == 'cop':
                place[1] = (place[1] - 1) % self.n
            self.matrix[place[0]][place[1]] = name 
            # Cop moves left, but robber stays

    def check_if_caught(self):
        if self.robber_location != self.cop_location:
            self.matrix[self.cop_location[0]][self.cop_location[1]] = self.cop_name
            return False
        elif self.robber_location == self.cop_location:
            self.matrix[self.robber_location[0]][self.robber_location[1]] = 3
            return True

    def again(self):
        while True:
            play_again = input('Play again? Enter y or n.').lower()
            if play_again in ('y','n'):
                break

        if play_again == 'n':
            exit() 
        elif play_again == 'y':
            return


DrunkenCopsAndRobbers(robber_drunk_percentage=.5,
                    cop_drunk_percentage=0,
                    robber_move_length=2,cop_move_length=1,
                    robber_location=(0,0),
                    cop_location='random',
                    run_multiple=False,number_of_games=50)

# robber_drunk_percentage and cop_drunk_percentage are the probability
# that the respective players move randomly

# robber_move_length and cop_move_length represent the number of moves
# the robber and cop are given each turn

# To manually place robber and cop, change robber_location and/or 
# cop_location from 'random', to tuples representing one or both's
# placement on a 0-indexed, mxn matrix.

# If you would like to calculate the average of a certain number of 
#cycles, change run_multiple to True and adjust the number_of_games 
# accordingly.

# Print statments have been made conditional on the run_multiple 
# variable in order to have a manageable output screen.
