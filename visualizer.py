import time
import sys
try:
    import pygame
except ImportError:
    pass

WALL_COLOR = (70, 70, 70)
BG_COLOR = (240, 240, 240)
PLAYER_COLOR = (50, 150, 250)
BOX_COLOR = (140, 90, 40)
GOAL_COLOR = (50, 200, 50)
BOX_ON_GOAL_COLOR = (100, 200, 100)

TILE_SIZE = 50

def run_visualization(game, path):
    if 'pygame' not in sys.modules:
        print("La librería 'pygame' no está instalada. Ejecutá 'pip install pygame' para la visualización.")
        return

    pygame.init()
    
    entities = game.walls | game.goals | game.initial_boxes | {game.player_start}
    max_r = max((r for r, c in entities), default=0)
    max_c = max((c for r, c in entities), default=0)

    width = (max_c + 2) * TILE_SIZE
    height = (max_r + 2) * TILE_SIZE

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban Visualizer - AI Solver")
    
    player, boxes = game.get_initial_state()
    boxes = set(boxes)
    
    directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

    def draw_state(current_player, current_boxes):
        screen.fill(BG_COLOR)
        
        for r, c in game.goals:
            pygame.draw.circle(screen, GOAL_COLOR, (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)
            
        for r, c in game.walls:
            pygame.draw.rect(screen, WALL_COLOR, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            
        for r, c in current_boxes:
            color = BOX_ON_GOAL_COLOR if (r, c) in game.goals else BOX_COLOR
            pygame.draw.rect(screen, color, (c * TILE_SIZE + 5, r * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
        
        pr, pc = current_player
        pygame.draw.circle(screen, PLAYER_COLOR, (pc * TILE_SIZE + TILE_SIZE // 2, pr * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 5)
        
        pygame.display.flip()

    draw_state(player, boxes)
    time.sleep(1)
    
    for action in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        dr, dc = directions[action]
        new_p = (player[0] + dr, player[1] + dc)
        
        if new_p in boxes:
            new_box = (new_p[0] + dr, new_p[1] + dc)
            boxes.remove(new_p)
            boxes.add(new_box)
            
        player = new_p
        
        draw_state(player, boxes)
        time.sleep(0.3)

    print("--- Visualización concluida ---")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()
