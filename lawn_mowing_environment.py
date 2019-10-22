import numpy as np

class environment():
    # this class defines what actions are available, what they do, and how they modify the environment
    # this class keeps track of the agents attributes including loss

    def __init__(self, agent_position, agent_direction, environment_shape):
        # position is a 2 element list containing a coordinate pair [x,y]
        # direction is a cardinal direction represented by one of the four characters N, S, E, W
        # environment_shape is the shape of the environment matrix
        
        self.environment_shape = environment_shape
        self.agent_position = agent_position
        self.agent_direction = agent_direction
        self.moves = 0
        
    def __can_occupy(self, tile):
        # can the agent occupy tile?
                
        return tile[0] != '9' # True if tile is not wood
    
    def __cut_the_grass(self, environment_state):        
        # if the current space is tall grass then cut it
        if environment_state[self.agent_position[0], self.agent_position[1]][0] == '8': # if current space is tall grass
            current_tile = environment_state[self.agent_position[0], self.agent_position[1]]
            environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '1', 0) # replace with cut grass     
        return environment_state
    
    def __modify_tile(self, tile, new_value, position):
        # returns tile with new_value in position
        # "why dont you just use arrays instead of non mutable strings?", mainly cause it makes one hot encoding easier but also cause
        # I already did it this way and am only now realizing making a tensor of the lawn instead of the matrix may bave been the better way.
        
        # converting to an array is slow with numpy.fromstring and slow with python list() so I decided to just not convert it
        if position == 0:
            return new_value + tile[1] + tile[2]
        elif position == 1:
            return tile[0] + new_value + tile[2] 
        elif position == 2:
            return tile[0] + tile[1] + new_value
        else:
            raise Exception('invalid tile index ' + position)
        
    def take_action(self, action, environment_state):
        # takes the action that was recived and returns an updated environment state
        
        if action == 1:
            updated_environment_state = self.advance(environment_state)
        elif action == 2:
            updated_environment_state = self.pivot_clockwise(environment_state)
        elif action == 3:
            updated_environment_state = self.pivot_counterclockwise(environment_state)
        else:
            raise Exception('invalid action_id ' + action)
        self.moves += 1        
        return updated_environment_state
    
    # below I define all actions the agent can take and how they modify the environment
    def advance(self, environment_state):
        # advance one space in the direction the agent is currently facing
        # return updated environment state
        
        current_tile = environment_state[self.agent_position[0], self.agent_position[1]] # defining here for readability
        
        if self.agent_direction == 'N':
            environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '1', 2) # exit from north
            if self.agent_position[0]-1 != -1 and self.__can_occupy(environment_state[self.agent_position[0]-1, self.agent_position[1]]): # if next space can be occupied
                self.agent_position[0] -= 1 # advance
                current_tile = environment_state[self.agent_position[0], self.agent_position[1]] # redefine current tile since the agent moved
                environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '2', 1) # exit from north # enter from south
        elif self.agent_direction == 'S':
            environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '2', 2) # exit from south
            if self.agent_position[0]+1 != self.environment_shape[0] and self.__can_occupy(environment_state[self.agent_position[0]+1, self.agent_position[1]]): # if next space can be occupied
                self.agent_position[0] += 1 # advance
                current_tile = environment_state[self.agent_position[0], self.agent_position[1]] # redefine current tile since the agent moved
                environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '1', 1) # enter from north
        elif self.agent_direction == 'E':
            environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '3', 2) # exit from east
            if self.agent_position[1]+1 != self.environment_shape[1] and self.__can_occupy(environment_state[self.agent_position[0], self.agent_position[1]+1]): # if next space can be occupied
                self.agent_position[1] += 1 # advance
                current_tile = environment_state[self.agent_position[0], self.agent_position[1]] # redefine current tile since the agent moved
                environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '4', 1) # enter from west
        elif self.agent_direction == 'W':
            environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '4', 2) # exit from west
            if self.agent_position[1]-1 != -1 and self.__can_occupy(environment_state[self.agent_position[0], self.agent_position[1]-1]): # if next space can be occupied
                self.agent_position[1] -= 1 # advance
                current_tile = environment_state[self.agent_position[0], self.agent_position[1]] # redefine current tile since the agent moved
                environment_state[self.agent_position[0], self.agent_position[1]] = self.__modify_tile(current_tile, '3', 1) # enter from east
        else:
            raise Exception('unknown direction')
        environment_state = self.__cut_the_grass(environment_state) # if the current space is tall grass then cut it
        return environment_state
    
    def pivot_clockwise(self, environment_state):
        # rotate direction by 90° clockwise
        # return updated environment state
        
        if self.agent_direction == 'N':
            self.agent_direction = 'E'
        elif self.agent_direction == 'S':
            self.agent_direction = 'W'
        elif self.agent_direction == 'E':
            self.agent_direction = 'S'
        elif self.agent_direction == 'W':
            self.agent_direction = 'N'
        else:
            raise Exception('unknown direction')        

        return environment_state
        
    def pivot_counterclockwise(self, environment_state):
        # rotate direction by 90° counterclockwise
        # return updated environment state
        
        if self.agent_direction == 'N':
            self.agent_direction = 'W'
        elif self.agent_direction == 'S':
            self.agent_direction = 'E'
        elif self.agent_direction == 'E':
            self.agent_direction = 'N'
        elif self.agent_direction == 'W':
            self.agent_direction = 'S'
        else:
            raise Exception('unknown direction')        
        
        return environment_state
    
    # below I define all getters which are just used to interface with the simulation class
    def get_done_condition(self, environment_state):
        # returns true if the environment is complete (entire lawn is mowed)
        
        return ('800' not in environment_state) # if there are no tall grass blocks then lawn is mowed
    
    def get_action_space(self):
        # returns tuple of possible actions as numbers
        # mapping:
        # 1 = 'advance'
        # 2 = 'pivot_clockwise'
        # 3 = 'pivot_counterclockwise'
        
        return (1,2,3)
        
    def get_position(self):
        # return agents current position
        return self.x, self.y
    
    def get_direction(self):
        # return agents current direction
        return self.direction
    
    def get_reward(self):
        # return agents current reward
        return -self.moves