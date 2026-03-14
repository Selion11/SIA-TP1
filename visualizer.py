import time
import sys
try:
    import pygame
except ImportError:
    pass

try:
    import numpy as np
    import imageio
    HAS_VIDEO_EXPORT = True
except ImportError:
    HAS_VIDEO_EXPORT = False

WALL_COLOR = (70, 70, 70)
BG_COLOR = (240, 240, 240)
PLAYER_COLOR = (50, 150, 250)
BOX_COLOR = (140, 90, 40)
GOAL_COLOR = (50, 200, 50)
BOX_ON_GOAL_COLOR = (100, 200, 100)
TEXT_COLOR = (255, 255, 255) # Nuevo color para el texto

TILE_SIZE = 50

# Ahora la función puede recibir el 'algorithm' directamente para buscar en tiempo real
def run_visualization(game, algorithm=None, precomputed_path=None, save_video=False, output_filename="solucion.gif"):
    if 'pygame' not in sys.modules:
        print("La librería 'pygame' no está instalada. Ejecutá 'pip install pygame'")
        return

    if save_video and not HAS_VIDEO_EXPORT:
        print("Para guardar video se requiere 'imageio' y 'numpy'. Continuando sin guardar...")
        save_video = False

    pygame.init()
    pygame.font.init() # Inicializamos las fuentes
    font = pygame.font.SysFont("Arial", 22, bold=True)
    
    entities = game.walls | game.goals | game.initial_boxes | {game.player_start}
    max_r = max((r for r, c in entities), default=0)
    max_c = max((c for r, c in entities), default=0)

    width = (max_c + 2) * TILE_SIZE
    height = (max_r + 2) * TILE_SIZE + 50 # +50px para la barra de estado superior

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sokoban Visualizer - AI Solver")
    
    player, boxes = game.get_initial_state()
    boxes = set(boxes)
    
    directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

    writer = None
    if save_video:
        fps = 1 / 0.3 
        writer = imageio.get_writer(output_filename, fps=fps)

    def capture_frame():
        if save_video and writer is not None:
            frame = pygame.surfarray.array3d(screen)
            frame = np.transpose(frame, (1, 0, 2))
            writer.append_data(frame)

    def draw_state(current_player, current_boxes, message=None):
        screen.fill(BG_COLOR)
        
        y_offset = 50 # Desplazamos el mapa hacia abajo para hacerle lugar al texto
        
        for r, c in game.goals:
            pygame.draw.circle(screen, GOAL_COLOR, (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2 + y_offset), TILE_SIZE // 4)
            
        for r, c in game.walls:
            pygame.draw.rect(screen, WALL_COLOR, (c * TILE_SIZE, r * TILE_SIZE + y_offset, TILE_SIZE, TILE_SIZE))
            
        for r, c in current_boxes:
            color = BOX_ON_GOAL_COLOR if (r, c) in game.goals else BOX_COLOR
            pygame.draw.rect(screen, color, (c * TILE_SIZE + 5, r * TILE_SIZE + 5 + y_offset, TILE_SIZE - 10, TILE_SIZE - 10))
        
        pr, pc = current_player
        pygame.draw.circle(screen, PLAYER_COLOR, (pc * TILE_SIZE + TILE_SIZE // 2, pr * TILE_SIZE + TILE_SIZE // 2 + y_offset), TILE_SIZE // 2 - 5)
        
        # Dibujamos la barra superior y el mensaje
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, width, 50))
        if message:
            text_surf = font.render(message, True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(width // 2, 25))
            screen.blit(text_surf, text_rect)
        
        pygame.display.flip()
        capture_frame()

    # --- 1. MOSTRAR ESTADO INICIAL ("Searching...") ---
    draw_state(player, boxes, "Searching... Please wait.")
    pygame.event.pump() # Evita que Windows/Mac digan que la ventana "No responde"
    
    path = precomputed_path
    
    # --- 2. EJECUTAR EL ALGORITMO Y MEDIR TIEMPO ---
    if algorithm is not None and path is None:
        start_time = time.time()
        path, nodes = algorithm.search(game)
        elapsed_time = time.time() - start_time
        
        if path is not None:
            success_msg = f"Solution found in {elapsed_time:.3f}s! ({nodes} nodes)"
            draw_state(player, boxes, success_msg)
        else:
            fail_msg = f"No solution found. Time: {elapsed_time:.3f}s"
            draw_state(player, boxes, fail_msg)
            time.sleep(3)
            pygame.quit()
            return
            
    # Pausa dramática para que el usuario lea el resultado
    time.sleep(2)
    
    if save_video:
        for _ in range(3): capture_frame()
    
    # --- 3. ANIMAR LA SOLUCIÓN ---
    step_count = 0
    for action in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if save_video and writer is not None:
                    writer.close()
                pygame.quit()
                return

        dr, dc = directions[action]
        new_p = (player[0] + dr, player[1] + dc)
        
        if new_p in boxes:
            new_box = (new_p[0] + dr, new_p[1] + dc)
            boxes.remove(new_p)
            boxes.add(new_box)
            
        player = new_p
        step_count += 1
        
        draw_state(player, boxes, f"Step {step_count}/{len(path)}: {action}")
        time.sleep(0.3)

    draw_state(player, boxes, "Finished!")
    
    if save_video and writer is not None:
        for _ in range(5): capture_frame()
        writer.close()
        print(f"--- ¡Archivo multimedia guardado exitosamente como '{output_filename}'! ---")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()