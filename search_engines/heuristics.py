def heuristic_manhattan(state, goals):
    _, boxes = state
    total_distance = 0
    for box in boxes:
        min_dist = min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in goals)
        total_distance += min_dist
    return total_distance

def heuristic_manhattan_player(state, goals):
    player, boxes = state
    total_box_distance = 0
    
    for box in boxes:
        min_dist = min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in goals)
        total_box_distance += min_dist
            
    player_to_box_dist = 0
    if boxes:
        closest_box_dist = min(abs(player[0] - box[0]) + abs(player[1] - box[1]) for box in boxes)
        player_to_box_dist = max(0, closest_box_dist - 1)
        
    return total_box_distance + player_to_box_dist