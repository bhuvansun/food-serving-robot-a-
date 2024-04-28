
# File to be executed. Others are support files used for the following:

# constants.py: stores the location of maps, images, step time, and min and max depths for IDS
# game_manager.py: algorithms for A*, IDS, BFS and Bi-directional BFS
# heap_hashtable.py: source code for minheap functions. Taken from github
# map.py: defines a map as a 2d array of string values such as 'x' denoting a blockade, 'r' denoting a robot and so on.
# node.py: defines the node of the state space, such as parent, child, depth, cost etc.
# state.py: defines the state space such as the robot position, items' position.
# screen_manager.py: uses the pygame library to start the simulation.

from game_manager import GameManager
import sys
import zipfile
import time

# Uploading zip file to Moodle and extracting maps and images from it
def unzip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

zip_file = 'stuff.zip'
extract_to = 'images_maps'
unzip(zip_file, extract_to)

def __main__():
    arg = sys.argv
    search_type = 'a_star' # Default search method
    if len(arg) > 1:
        if arg[1] in ['a_star', 'ids', 'bfs', 'bd_bfs']:
            search_type = arg[1]
        else:
            print('\n\nUse "ids" or "a_star" or "bd_bfs" as argument.')
            return

    game_manager = GameManager()

    # Implementing selected search algorithm
    start_time = time.time()
    result, depth, cost = game_manager.start_search(search_type)
    end_time = time.time()
    time_taken = end_time - start_time

    directions = {
        (1, 0): 'D', 
        (-1, 0): 'U', 
        (0, 1): 'R', 
        (0, -1): 'L'
    }  
    
    # Initial state
    p1 = game_manager.init_state.robot

    # Printing directions
    for i in range(len(result)):
        p2 = result[i].robot
        print(directions[(p2[0] - p1[0], p2[1] - p1[1])], end = '')
        # print(p2, p1, directions[(p2[0]-p1[0], p2[1]-p1[1])]) # Before move, after move, directions
        p1 = result[i].robot # Update current coordinate of robot

    print('\nTotal moves:', depth)
    print('Total cost:', cost)
    print("Time taken:", time_taken, "seconds")
    game_manager.display_states(result)

__main__()
