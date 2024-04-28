from map import Map

class State:

    def __init__(self, robot: tuple, items=[]):
        self.robot = robot
        self.items = items

    def __eq__(self, other):
        return self.items == other.items and self.robot == other.robot

    def __str__(self):
        return '"Robot at: ' + str(self.robot) + ' items at: ' + str(self.items) + '"'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):

        h = hash(self.robot)
        for i in self.items:
            h += hash(i)
        return h

    @staticmethod
    def successor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:

        map_array = map_object.map
        points = map_object.points
        w, h = map_object.w, map_object.h
        next_states = []
        robot_y, robot_x = state.robot[0], state.robot[1]

        def try_move_robot(y: int, x: int):

            if x * y != 0:
                raise Exception('Error: Cannot move diagonally')

            if map_object.check_out_of_bounds(robot_y + y, robot_x + x):
                return

            if map_object.is_block(robot_y + y, robot_x + x):
                return

            if (robot_y + y, robot_x + x) not in state.items:
                next_states.append((
                    State((robot_y + y, robot_x + x), state.items.copy()),
                    (y, x),
                    max(int(map_array[robot_y + y][robot_x + x]), int(map_array[robot_y][robot_x]))
                ))
            else:
                if (y == -1 and robot_y != 1) or (y == 1 and robot_y != h - 2) or \
                        (x == -1 and robot_x != 1) or (x == 1 and robot_x != w - 2):

                    if (robot_y + y, robot_x + x) in points:
                        return

                    r2y, r2x = robot_y + 2 * y, robot_x + 2 * x
                    if map_object.is_block(r2y, r2x) or ((r2y, r2x) in state.items):
                        return

                    new_items = state.items.copy()
                    new_items.remove((robot_y + y, robot_x + x))
                    new_items.append((r2y, r2x))
                    next_states.append((
                        State((robot_y + y, robot_x + x), new_items),
                        (y, x),
                        max(int(map_array[robot_y + y][robot_x + x]), int(map_array[robot_y][robot_x]))
                    ))

        try_move_robot(1, 0)
        try_move_robot(0, 1)
        try_move_robot(-1, 0)
        try_move_robot(0, -1)

        return next_states

    @staticmethod
    def predecessor(state: 'State', map_object: Map) -> list[tuple['State', tuple, int]]:
        next_states = []
        robot_y, robot_x = state.robot[0], state.robot[1]

        def try_move_robot(y: int, x: int):

            if x * y != 0:
                raise Exception('Error: Cannot move diagonally')

            if map_object.check_out_of_bounds(robot_y + y, robot_x + x):
                return

            if map_object.is_block(robot_y + y, robot_x + x):
                return

            if (robot_y + y, robot_x + x) in state.items:
                return

            next_states.append((
                State((robot_y + y, robot_x + x), state.items.copy()),
                (y, x),
                max(int(map_object.map[robot_y + y][robot_x + x]), int(map_object.map[robot_y][robot_x]))
            ))

            if (robot_y - y, robot_x - x) in state.items:
                new_items = state.items.copy()
                new_items.remove((robot_y - y, robot_x - x))
                new_items.append((robot_y, robot_x))
                next_states.append((
                    State((robot_y + y, robot_x + x), new_items),
                    (y, x),
                    max(int(map_object.map[robot_y + y][robot_x + x]), int(map_object.map[robot_y][robot_x]))
                ))

        try_move_robot(1, 0)
        try_move_robot(0, 1)
        try_move_robot(-1, 0)
        try_move_robot(0, -1)

        return next_states

    @staticmethod
    def is_goal(state: 'State', points: list[tuple]):
        
        for item in state.items:
            if item not in points:
                return False
        return True
