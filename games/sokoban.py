class SokobanGame:
    def __init__(self, map_data):
        self.walls = set()
        self.goals = set()
        self.initial_boxes = []
        self.player_start = None

        for r, row in enumerate(map_data):
            for c, char in enumerate(row):
                if char == '#':
                    self.walls.add((r, c))
                elif char == '.':
                    self.goals.add((r, c))
                elif char == '@':
                    self.player_start = (r, c)
                elif char == '+':
                    self.player_start = (r, c)
                    self.goals.add((r, c))
                elif char == '$':
                    self.initial_boxes.append((r, c))
                elif char == '*':
                    self.initial_boxes.append((r, c))
                    self.goals.add((r, c))

    def get_initial_state(self):
        return self.player_start, tuple(self.initial_boxes)

    def is_goal(self, state):
        _, boxes = state
        return set(boxes) == self.goals

    def _is_corner_deadlock(self, r, c):
        """
        Detecta si una posición (r, c) es un deadlock de esquina (corner deadlock).
        Devuelve True si la caja en esa posición está bloqueada irremediablemente.
        """
        if (r, c) in self.goals:
            return False

        wall_up = (r - 1, c) in self.walls
        wall_down = (r + 1, c) in self.walls
        wall_left = (r, c - 1) in self.walls
        wall_right = (r, c + 1) in self.walls

        if wall_up and wall_left: return True
        if wall_up and wall_right: return True
        if wall_down and wall_left: return True
        if wall_down and wall_right: return True

        return False

    def get_successors(self, state):
        """
        Genera los siguientes estados válidos a partir del estado actual.
        INCLUYE PODA POR DEADLOCKS DE ESQUINA.
        """
        player, boxes = state
        successors = []
        directions = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        for action, (dr, dc) in directions.items():
            new_r, new_c = player[0] + dr, player[1] + dc
            new_p = (new_r, new_c)

            if new_p in self.walls:
                continue

            if new_p in boxes:
                new_box_r, new_box_c = new_r + dr, new_c + dc
                new_box = (new_box_r, new_box_c)

                if new_box in self.walls or new_box in boxes:
                    continue

                if self._is_corner_deadlock(new_box_r, new_box_c):
                    continue

                new_boxes_list = list(boxes)
                new_boxes_list.remove(new_p)
                new_boxes_list.append(new_box)
                new_boxes = tuple(new_boxes_list)
                
                successors.append(((new_p, new_boxes), action))
            
            else:
                successors.append(((new_p, boxes), action))

        return successors