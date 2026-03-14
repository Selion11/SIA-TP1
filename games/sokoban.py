class SokobanGame:
    def __init__(self, map_data):
        self.walls = set()
        self.goals = set()
        self.initial_boxes = set()
        self.player_start = None
        self._parse_map(map_data)

    def _parse_map(self, map_data):
        for r, row in enumerate(map_data):
            for c, char in enumerate(row):
                if char == '#': self.walls.add((r, c))
                elif char == '.': self.goals.add((r, c))
                elif char == '$': self.initial_boxes.add((r, c))
                elif char == '@': self.player_start = (r, c)
                elif char == '*':
                    self.initial_boxes.add((r, c))
                    self.goals.add((r, c))

    def get_initial_state(self):
        return (self.player_start, frozenset(self.initial_boxes))

    def is_goal(self, state):
        _, boxes = state
        return self.goals == boxes

    def get_successors(self, state):
        player, boxes = state
        successors = []
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

        for action, (dr, dc) in directions.items():
            new_p = (player[0] + dr, player[1] + dc)
            
            if new_p in self.walls: continue
            
            if new_p in boxes:
                new_box = (new_p[0] + dr, new_p[1] + dc)
                if new_box not in self.walls and new_box not in boxes:
                    new_boxes = set(boxes)
                    new_boxes.remove(new_p)
                    new_boxes.add(new_box)
                    successors.append(((new_p, frozenset(new_boxes)), action))
            else:
                successors.append(((new_p, boxes), action))
        return successors