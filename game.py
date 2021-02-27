import numpy as np
import random

class DrunkenCopsAndRobbers:
    def __init__(self,rob_drunk_pct=.5,cop_drunk_pct=.5,rob_move_len=1,
                cop_move_len=1,diagonal_move=True,pass_move=True,
                ply_before_robber_spawn=-1,rob_loc='random',
                cop_loc='random',multi_game=False,num_of_games=50,
                max_iter_per_game=1000):

        self.rob_drunk_pct = rob_drunk_pct
        self.rob_move_len = rob_move_len
        self.cop_drunk_pct = cop_drunk_pct
        self.cop_move_len = cop_move_len
        self.diagonal_move = diagonal_move
        self.pass_move = pass_move
        self.multi_game = multi_game
        self.num_of_games = num_of_games
        self.max_iter_per_game = max_iter_per_game
        self.ply_before_robber_spawn = ply_before_robber_spawn

        self.check_parameters()

        run_count = 0
        results_list = []
        win_list = []

        self.robber_name,self.cop_name = 1,2
        self.move_list = []
        self.fill_move_list(diagonal_move,pass_move)

        self.m,self.n = 0,0
        self.get_matrix_dimensions()

        while True:
            self.iteration_count = 0
            self.matrix = self.create_matrix()

            self.placement_list = []
            if rob_loc == 'random' or cop_loc == 'random':
                self.fill_placement_list()

            self.rob_loc_list = []
            self.rob_loc_list.append(
                                self.place(rob_loc,self.robber_name)
                                    )

            self.cop_loc = self.place(cop_loc,self.cop_name)

            if not multi_game:
                self.print_locations()

            grid_size = self.m * self.n
            while 0 < len(self.rob_loc_list) < grid_size:
                if (ply_before_robber_spawn >= 1
                    and self.iteration_count != 0 
                    and self.iteration_count 
                        % self.ply_before_robber_spawn == 0):

                    self.rob_loc_list.append(
                                self.place(rob_loc,self.robber_name)
                                            )
                
                self.start_chase()
                self.iteration_count += 1

                if not multi_game:
                    self.print_locations()
                
                if self.iteration_count == max_iter_per_game:
                    break

            if (self.iteration_count == max_iter_per_game 
                and not multi_game):
                print('The game reached the max_iteration_count')
            elif (not multi_game 
                and len(self.rob_loc_list) < grid_size):
                print('The cop caught the robber(s).')
                print('It took '+ str(self.iteration_count) 
                        +' iterations.')
            elif not multi_game:
                print('The robbers won this round.')
                print('It took '+ str(self.iteration_count) 
                        +' iterations.')
        
            # If multi_game=True, don't comment out print statements
            # below this point.
            if multi_game:
                if run_count < num_of_games:
                    results_list.append(self.iteration_count)
                    run_count += 1
                    if len(self.rob_loc_list) < grid_size:
                        win_list.append(2)
                    else:
                        win_list.append(1)
                else: #run_count > num_of_games:
                    print('Over',num_of_games,'games,')
                    print('the average iteration was',
                            np.mean(results_list))
                    print('List of iterations during test:\n',
                            results_list,'\n')
                    print('The cops won', 
                        win_list.count(2) / num_of_games * 100,
                        'percent of the time')
                    print('List of win results:\n',win_list,'\n')
                    self.again()
                    run_count = 0
                    results_list = []
            else:
                self.again()

    def check_parameters(self):
        flag = False
        if not (type(self.rob_drunk_pct) in (float,int) 
            and 0 <= self.rob_drunk_pct <= 1):
            print('rob_drunk_pct must be a number between 0 and 1.')
            flag = True
        if not (type(self.cop_drunk_pct) in (float,int) 
            and 0 <= self.cop_drunk_pct <= 1):
            print('cop_drunk_pct must be a number between 0 and 1.')
            flag = True
        if not (type(self.rob_move_len) in (float,int)
            and self.rob_move_len >= 1):
            print('rob_move_len must be a number >= 1.')
            flag = True
        else:
            self.rob_move_len = int(self.rob_move_len)
        if not (type(self.cop_move_len) in (float,int)
            and self.cop_move_len >= 1):
            print('cop_move_len must be a number >= 1.')
            flag = True
        else:
            self.cop_move_len = int(self.cop_move_len)
        if type(self.diagonal_move) != bool:
            print('diagonal_move must be a bool.')
            flag = True
        if type(self.pass_move) != bool:
            print('pass_move must be a bool.')
            flag = True
        if type(self.multi_game) != bool:
            print('multi_game must be a bool.')
            flag = True
        if not (type(self.num_of_games) in (float,int)
            and self.num_of_games >= 1):
            print('num_of_games must be a number >= 1.')
            flag = True
        else:
            self.num_of_games = int(self.num_of_games)
        if not (type(self.max_iter_per_game) in (float,int)
            and self.max_iter_per_game >= 1):
            print('max_iter_per_game must be a number >= 1.')
            flag = True
        else:
            self.max_iter_per_game = int(self.max_iter_per_game)
        if not (type(self.ply_before_robber_spawn) == int
            and (self.ply_before_robber_spawn == -1
                or self.ply_before_robber_spawn >= 1)):
            print('ply_before_robber_spawn must be -1 '
                    + 'or an integer >= 1.')
            flag = True

        if flag:
            exit()

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

    def fill_move_list(self,diagonal_move,pass_move):
        for a in range(-1,2):
            for b in range(-1,2):
                self.move_list.append((a,b))
        
        if not diagonal_move: # Vertical and horizontal only
            self.move_list.remove((1,1))
            self.move_list.remove((1,-1))
            self.move_list.remove((-1,1))
            self.move_list.remove((-1,-1))

        if not pass_move:
            self.move_list.remove((0,0))

    def fill_placement_list(self):
        for a in range(self.m):
            for b in range(self.n):
                self.placement_list.append((a,b))

    def print_matrix(self):
        print('Iteration:',self.iteration_count)
        print(self.matrix,'\n')

    def print_locations(self):
        self.print_matrix()
        print('Locations:\n',
                'robber(s):',self.rob_loc_list,'\n',
                'robber count:',len(self.rob_loc_list),'\n',
                'cop:',self.cop_loc,'\n'*2)

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

    def start_chase(self):
        # TODO for robber on board (when multiple robbers spawn in)
        for self.i,self.rob_loc in enumerate(self.rob_loc_list):
            for turn in range(self.rob_move_len):    
                purposeful = self.get_drunkenness('rob')
                if purposeful:
                    self.get_direction('rob')
                    # Robber avoids cop
                else:
                    self.make_random_move('rob') 
                    # Robber randomly moves 
                caught = self.check_if_caught('rob')
                if caught:
                    break
        if len(self.rob_loc_list) == 0:
            return
        # TODO for cop on board (when multiple cops spawn in)
        for turn in range(self.rob_move_len):
            purposeful = self.get_drunkenness('cop')
            if purposeful:  
                self.get_direction('cop') # Cop chases robber        
            else: 
                self.make_random_move('cop') 
                # Cop randomly moves
            caught = self.check_if_caught('cop')
            if caught and not len(self.rob_loc_list):
                break


    def get_drunkenness(self,player_string):
        place,name,drunk = self.get_side(player_string)
        purposeful = random.choices([False,True],[drunk,1-drunk])
        if not self.multi_game:
            if player_string == 'cop':
                print('Move: cop')
            else:
                print('Move: rob',self.i)
            print('purposeful:',purposeful[0])
            print('place:',place,'\n')
        return purposeful[0]

    def get_side(self,player_string):
        if player_string.lower() == 'rob':
            place = self.rob_loc
            name = self.robber_name
            drunk = self.rob_drunk_pct
        elif player_string.lower() == 'cop':
            place = self.cop_loc
            name = self.cop_name
            drunk = self.cop_drunk_pct
        return place,name,drunk

    def make_random_move(self,player_string): 
    # Finds possible move for player
        if player_string == 'rob':
            self.matrix[tuple(self.rob_loc)] = 0 
            # Removes previous location
            self.move(self.rob_loc,self.robber_name)   
        elif player_string == 'cop':
            self.matrix[tuple(self.cop_loc)] = 0 
            # Removes previous location
            self.move(self.cop_loc,self.cop_name)

    def move(self,place,name):
        move_tuple = random.choice(self.move_list)
        place[0] = (place[0] + move_tuple[0]) % self.m
        place[1] = (place[1] + move_tuple[1]) % self.n 
        if not self.multi_game:
            print('Up/Down:',move_tuple[0],'to',place[0])  
            print('Side/Side:',move_tuple[1],'to',place[1],'\n')
        self.matrix[tuple(place)] = name 

    def get_direction(self,player_string): 
    # Cop chase robber and/or robber avoids cop.
        place,name,drunk = self.get_side(player_string)
        rob_loc = self.rob_loc
        cop_loc = self.cop_loc
        self.matrix[tuple(place)] = 0 
        # Removes robber/cop's previous location
        #vertical
        if ((rob_loc[0] - cop_loc[0]) % self.m 
            > (cop_loc[0] - rob_loc[0]) % self.m):
            
            place[0] = (place[0] - 1) % self.m # Player moves up
        elif ((rob_loc[0] - cop_loc[0]) % self.m 
            < (cop_loc[0] - rob_loc[0]) % self.m):
            
            place[0] = (place[0] + 1) % self.m # Player moves down
        elif (rob_loc[0] - cop_loc[0]) % self.m == 0: 
            # Catches where cop and robber are on same row
            if player_string == 'rob':
                place[0] = (place[0] - 1) % self.m 
                # Robber moves up, but cop stays
        elif ((rob_loc[0] - cop_loc[0]) % self.m 
            == (cop_loc[0]  - rob_loc[0]) % self.m):
            if player_string == 'cop':
                place[0] = (place[0] - 1) % self.m 
                # Cop moves up, but robber stays
        #horizontal
        if ((rob_loc[1] - cop_loc[1]) % self.n 
            > (cop_loc[1] - rob_loc[1]) % self.n):
            place[1] = (place[1] - 1) % self.n
            self.matrix[tuple(place)] = name # Player moves left
        elif ((rob_loc[1] - cop_loc[1])%self.n 
            < (cop_loc[1] - rob_loc[1]) % self.n):
            place[1] = (place[1]+1)%self.n
            self.matrix[tuple(place)] = name # Player moves right
        elif (rob_loc[1] - cop_loc[1]) % self.n == 0: 
            # Catches where cop and robber are on same column
            if player_string == 'rob':
                place[1] = (place[1] - 1) % self.m 
                # Robber moves left, but cop stays
            self.matrix[tuple(place)] = name
        elif ((rob_loc[1] - cop_loc[1]) % self.n 
            == (cop_loc[1] - rob_loc[1]) % self.n):
            if player_string == 'cop':
                place[1] = (place[1] - 1) % self.n
            self.matrix[tuple(place)] = name 
            # Cop moves left, but robber stays

    def check_if_caught(self,player_string):
        if self.cop_loc not in self.rob_loc_list:
            self.matrix[tuple(self.cop_loc)] = self.cop_name
            return False
        elif player_string == 'rob' and self.rob_loc == self.cop_loc:
            self.matrix[tuple(self.rob_loc)] = 3
            self.rob_loc_list.remove(self.rob_loc) 
            print('CAUGHT! The robber landed on the cop')
            return True
        elif (player_string == 'cop' and self.cop_loc in   
            self.rob_loc_list):
            self.matrix[tuple(self.cop_loc)] = 3
            self.rob_loc_list.remove(self.cop_loc) 
            print('CAUGHT! The cop landed on a robber')
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


DrunkenCopsAndRobbers(rob_drunk_pct=.5,cop_drunk_pct=.5,rob_move_len=1,
                cop_move_len=1,diagonal_move=True,pass_move=True,
                ply_before_robber_spawn=-1,rob_loc='random',
                cop_loc='random',multi_game=False,num_of_games=50,
                max_iter_per_game=100)
