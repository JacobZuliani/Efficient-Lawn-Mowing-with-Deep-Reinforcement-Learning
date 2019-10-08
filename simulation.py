import numpy as np
from copy import deepcopy
from visualization import visualize_environment

class simulation():
    # this class manages the simulation for any agent or environment

    def __init__(self, starting_environment_state, environment, visualization):
        # environment is a class instance defining what the agent can and can't do
        # visualization is an instance of visualize_environment from visualization.py
        # starting_environment_state is the starting view of the environment (matrix of strings)
        
        # below variables should not be modified
        self.starting_visualization = visualization # class instance
        self.starting_environment = environment # class instance
        self.starting_environment_state = starting_environment_state # matrix of strings
        self.reset()
        
    def get_action_space(self):
        # returns a tuple of functions where each function defines the action
        
        return self.environment.get_action_space()
    
    def get_simulation_history_visualization(self, file_name, fps):
        # outputs an mp4 file of the agent mowing the lawn
        
        self.visualization.output_history(file_name, fps)
        
    def display_last_env_state(self):
        # displays the last environment state of the simulation
        
        self.visualization.display_last_environment_state()
    
    def reset(self):
        # resets environment to the way it was when the simulation was initalized
        # returns the starting environment state
        
        # everything needs to be copied (instead of creating another pointer) to avoid modifying the original
        self.current_environment_state = deepcopy(self.starting_environment_state)
        self.visualization = deepcopy(self.starting_visualization)
        self.environment = deepcopy(self.starting_environment)
        self.reward = 0
        return self.current_environment_state
        
    def step(self, action):
        # competes single environment step where agent takes action, then recives observation, reward, and whether they are done
        
        self.current_environment_state = self.environment.take_action(action, self.current_environment_state) # take action to get next environment state
        self.reward = self.environment.get_reward() # obtain current reward
        self.visualization.recive_environment_state(self.current_environment_state) # update visualization
        # return updated environment state, reqard, and done_condition
        return self.current_environment_state, self.reward, self.environment.get_done_condition(self.current_environment_state)
    
def show_environment_state(environment_state):
    # shows any environment state inde
    
    visualization = visualize_environment()
    visualization.recive_environment_state(environment_state)
    visualization.display_last_environment_state()