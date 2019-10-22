import numpy as np

# one hot encode each tile into 5 possible categories:
# index 0: cut_grass
# index 1: tall_grass
# index 2: pavement
# index 3: wood
# index 4: agent
# I chose to exclude all arrows to simplify the input

def one_hot_encode_tile(tile): # given single tile returns one hot encoding
    
    if (tile[0][1] != '0') and (tile[0][2] == '0'): # if agent
        return np.array([0, 0, 0, 0, 1])
    if tile[0][0] == '1': # if cut_grass
        return np.array([1, 0, 0, 0, 0])
    elif tile[0][0] == '8': # if tall_grass
        return np.array([0, 1, 0, 0, 0])
    elif tile[0][0] == '2': # if pavement
        return np.array([0, 0, 1, 0, 0])
    elif tile[0][0] == '9': # if wood
        return np.array([0, 0, 0, 1, 0])
    else:
        raise Exception('invalid tile_id ' + tile)
        
def one_hot_encode_environment_state(environment_state):
    # produces matrix of shape ((environment_x_dim * environment_y_dim), num_categories_in_ohe) with tiles on the x axis and the ohe tile category on the y axis
    # applies the one_hot_encode_tile function on every tile
    
    return np.apply_along_axis(one_hot_encode_tile, 1, np.expand_dims(environment_state.flatten(), 1)).astype('float')