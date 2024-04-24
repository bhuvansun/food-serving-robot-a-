from game_manager import GameManager
import sys

def __main__():
    arg = sys.argv
    search_type = 'a_star'
    if len(arg) > 1:
        if arg[1] in ['ids', 'a_star', 'bd_bfs', 'reverse_bfs', 'bfs']:
            search_type = arg[1]
        else:
            print('\n\nUse "ids" or "a_star" or "bd_bfs" as argument.')
            return

    game_manager = GameManager()

    # Implementing selected search algorithm
    result, depth, cost = game_manager.start_search(search_type)

    # Printing outputs
    directions = {
        (1, 0): 'D', 
        (-1, 0): 'U', 
        (0, 1): 'R', 
        (0, -1): 'L'
                 }
    
    p1 = game_manager.init_state.robot

    for i in range(len(result)):
        p2 = result[i].robot
        print(directions[(p2[0]-p1[0], p2[1]-p1[1])], end = '')
        # print(p2, p1, (p2[0]-p1[0], p2[1]-p1[1]))
        p1 = result[i].robot

    print('\nTotal moves:', depth)
    print('Total cost:', cost)
    game_manager.display_states(result)

__main__()
