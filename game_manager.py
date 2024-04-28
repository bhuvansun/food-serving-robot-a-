from map import Map
from constants import Consts
from screen_manager import Display
from state import State
from node import Node
from heap_hashtable import MinHeap
import time

# Reading map given as a text file
def read_line_by_line(file_name: str) -> list[list[str]]:
        
        result = []
        with open(file_name, 'r') as map_file:
            for row in map_file:
                result.append(row.split())
        return result

class GameManager:

    map: Map
    init_state: State
    display: Display

    def __init__(self):

        self.map, self.init_state = self.parse_map()
        self.display = Display(self.map)

    def start_search(self, search_type: str) -> (list[State], int, int): # type: ignore
        result = self.__getattribute__(search_type + '_search')()

        if search_type in ['bd_bfs', 'reverse_bfs']:
            return result
        else:
            result_list = GameManager.extract_path_list(result)
            result_list.pop()
            result_list.reverse()
            return result_list, result.depth, result.path_cost

    def display_states(self, states_list: list[State]) -> None:

        if len(states_list) <= 0:
            print('There is nothing we can do')
            return
        
        self.display.update(self.init_state)
        self.display.begin_display()

        for state in states_list:
            time.sleep(Consts.STEP_TIME)
            self.display.update(state)

    # A* search
    def a_star_search(self) -> Node:

        # Euclid Distance as Cost function
        def euclid_distance(point1: tuple[int, int], point2: tuple[int, int]) -> float:            
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        
        # Manhattan Distance as Heuristic function
        def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
            
            d1 = point1[0] - point2[0]
            d2 = point1[1] - point2[1]
            if d1 < 0:
                d1 *= -1
            if d2 < 0:
                d2 *= -1
            return d1 + d2
        
        def heuristic(state: State) -> int:

            sum_of_distances = 0
            for item in state.items:
                min_d_to_point = float('inf')
                for point in self.map.points:
                    h = manhattan_distance(point, item)
                    if h < min_d_to_point:
                        min_d_to_point = h
                 # f(n) = g(n) + h(n)
                sum_of_distances += min_d_to_point + euclid_distance(point, item)

            return sum_of_distances
        
        Node.heuristic = heuristic

        # Beginning of A* search
        heap = MinHeap()
        visited = set()
        root_node = Node(self.init_state)
        heap.add(root_node)
        while not heap.is_empty():
            node = heap.pop()

            if State.is_goal(node.state, self.map.points):
                return node

            if node.state not in visited:
                visited.add(node.state)
            else:
                continue

            actions = State.successor(node.state, self.map)
            for child in node.expand(actions):
                heap.add(child)

    # Iterative Deepening Search
    def ids_search(self) -> Node:
        
        # For each depth (Depth Limited Search)
        def dls_search(limit: int, depth: int, node: Node) -> Node:

            if time.time() - cur_time > 30.0:
                raise Exception('Time limit exceeded')

            res = None
            if depth < limit and node.state not in visited_states:
                actions = State.successor(node.state, self.map)
                # print(actions)
                visited_states[node.state] = True
                for child in node.expand(actions)[::-1]:

                    if State.is_goal(child.state, self.map.points):
                        return child
                    
                    r = dls_search(limit, depth + 1, child)
                    if r is not None:
                        res = r
                        break

                    if child.state in visited_states:
                        del visited_states[child.state]

            return res
        
        # Iteration for IDS
        for i in range(Consts.FIRST_K, Consts.LAST_K):
            print('Starting with depth', i)
            cur_time = time.time()
            root_node = Node(self.init_state)
            visited_states = {}
            result = dls_search(i, 0, root_node)
            if result is not None:
                return result
    
    # BFS
    def bfs_search(self) -> Node:

        queue = [Node(self.init_state)]
        visited = {}

        while len(queue) > 0:
            node_1 = queue.pop(0)
            visited[node_1.state] = node_1

            if State.is_goal(node_1.state, self.map.points):
                return node_1
            
            actions = State.successor(node_1.state, self.map)
            for child in node_1.expand(actions):
                if child.state not in visited:
                    queue.append(child)

    # Bi-directional BFS
    def bd_bfs_search(self) -> (list[Node], int, int): # type: ignore

        # Bi-directional BFS for two nodes
        def bd_bfs(init: State, goal: State) -> (Node, Node): # type: ignore

            init_node = Node(init)
            goal_node = Node(goal)
            queue1 = [Node(init)]
            queue2 = [Node(goal)]
            visited1 = {init: init_node}
            visited2 = {goal: goal_node}

            while len(queue1) > 0 and len(queue2) > 0:
                node_1 = queue1.pop(0)
                node_2 = queue2.pop(0)

                if node_2.state in visited1:
                    return visited1[node_2.state], node_2
                
                if node_1.state in visited2:
                    return node_1, visited2[node_1.state]

                actions = State.successor(node_1.state, self.map)
                for child in node_1.expand(actions):
                    if child.state not in visited1:
                        queue1.append(child)
                        visited1[child.state] = child
                
                actions = State.predecessor(node_2.state, self.map)
                for child in node_2.expand(actions):
                    if child.state not in visited2:
                        queue2.append(child)
                        visited2[child.state] = child

            return None, None

        new_points = self.init_state.items.copy()
        for i, point in enumerate(self.map.points):
            new_points[i] = point

        all_goal_states = []
        for i, point in enumerate(self.map.points):
            for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_y = point[0] + direction[0]
                new_x = point[1] + direction[1]

                if self.map.check_out_of_bounds(new_y, new_x) or self.map.is_block(new_y, new_x):
                    continue

                if (new_y, new_x) in new_points:
                    continue

                state = State((new_y, new_x), new_points.copy())
                all_goal_states.append(state)
        
        shortest_list = []
        shortest_length = float('inf')
        shortest_path_cost = float('inf')

        print('Found', len(all_goal_states), 'possible ways.')
        for goal_state in all_goal_states:
            node1, node2 = bd_bfs(self.init_state, goal_state)
            if node1 is None or node2 is None:
                continue

            result_list = GameManager.extract_path_list(node1)
            result_list.reverse()
            result_list.pop()
            result_list.pop(0)
            result_list.extend(GameManager.extract_path_list(node2))

            if len(result_list) < shortest_length:
                print('Found a way with', len(result_list), 'moves.')
                shortest_length = len(result_list)
                shortest_list = result_list
                shortest_path_cost = node1.path_cost + node2.path_cost

        return shortest_list, shortest_length, shortest_path_cost

    @staticmethod
    def parse_map() -> (Map, State): # type: ignore

        map_array = read_line_by_line(Consts.MAP_FILE)
        sizes = map_array.pop(0)
        h, w = int(sizes[0]), int(sizes[1])
        map_object = Map(h, w)

        items = []
        points = []
        robot = (0, 0)
        for j, row in enumerate(map_array):
            for i, col in enumerate(row):

                if len(col) > 1:
                    if col[1] == 'b':
                        items.append((j, i))
                    elif col[1] == 'p':
                        points.append((j, i))
                    elif col[1] == 'r':
                        robot = (j, i)
                    row[i] = col[0]
            
            map_object.append_row(row)

        map_object.set_points(points)
        return map_object, State(robot, items)

    @staticmethod
    def extract_path_list(node: Node) -> list[State]:

        result_list = []
        watchdog = 0
        while node is not None:
            watchdog += 1
            if watchdog > 1000:
                raise Exception('Watchdog limit exceeded')
            result_list.append(node.state)
            node = node.parent

        return result_list

    @staticmethod
    def state_in_list_of_nodes(state: State, nodes_list: list[Node]) -> bool:
        for node in nodes_list:
            if node.state == state:
                return True
        return False
