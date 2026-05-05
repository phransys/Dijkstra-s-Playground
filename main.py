import pygame
import math
from levels import levels
from dijkstra import dijkstra, reconstruct_path
from menu import show_menu

pygame.init()
clock = pygame.time.Clock()

#color scheme 
BG = (28, 24, 20)
STONE = (55, 48, 42)
BRONZE = (120, 90, 50)
GOLD = (190, 150, 70)
EMBER = (220, 120, 40)
BLOOD = (140, 40, 30)
MOSS = (80, 110, 70)
PARCHMENT = (220, 210, 180)
NORMAL = (140, 120, 90)
PATH = (240, 170, 60)

game_state = "PLAYING"
big_font = pygame.font.SysFont("arial", 60)

def draw_star(surface, color, center, size, glow=False):
    #make star glow
    if glow:
        for i in range(3):
            glow_radius = size + (i*6)
            glow_color = (255, 200, 100, 40 - i*10)

            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, glow_color, (glow_radius,glow_radius), glow_radius)
            surface.blit(glow_surf, (center[0] - glow_radius, center[1] - glow_radius))

    #star shape
    points = []
    for i in range(10):
        angle = i * (math.pi / 5)
        radius = size if i % 2 == 0 else size // 2
        x = center[0] +radius * math.sin(angle)
        y = center[1] - radius * math.cos(angle)
        points.append((x, y))
    
    pygame.draw.polygon(surface, color, points)

WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Playground")

font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont(None, 24)

level_index = 0
score = 0

#menu
if not show_menu(screen, WIDTH, HEIGHT):
    pygame.quit()
    exit()


#helpers 
def load_level(index):
    level = levels[index]
    return level, [level["start"]], 0, False, False, set()


def get_clicked_node(mouse_pos, nodes):
    for node, pos in nodes.items():
        if math.dist(mouse_pos, pos) < 35:
            return node
    return None


def valid_move(graph, current, target):
    for neighbor, weight in graph[current]:
        if neighbor == target:
            return weight
    return None


#initialize game state
level, player_path, player_weight, finished, has_key, collected_treasures = load_level(level_index)

running = True
while running:
    screen.fill(BG)

    pulse = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
    # background grid
    for x in range(0, WIDTH, 80):
        for y in range(0, HEIGHT, 80):
            pygame.draw.rect(screen, STONE, (x, y, 78, 78), 1)

    graph = level["graph"]
    raw_nodes = level["nodes"]
    Y_OFFSET = 120

    nodes = {
        node: (pos[0], pos[1] + Y_OFFSET)
        for node, pos in raw_nodes.items()
    }

    #draw edges
    drawn = set()
    for node in graph:
        for neighbor, weight in graph[node]:
            if (neighbor, node) not in drawn:
                x1, y1 = nodes[node]
                x2, y2 = nodes[neighbor]

                pygame.draw.line(screen, (80, 70, 60), (x1, y1), (x2, y2), 6)
                pygame.draw.line(screen, BRONZE, (x1, y1), (x2, y2), 2)

                mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                txt = small_font.render(str(weight), True, (255, 255, 0))
                screen.blit(txt, (mx, my))

                drawn.add((node, neighbor))

    #draw player path
    for i in range(len(player_path) - 1):
        start_pos = nodes[player_path[i]]
        end_pos = nodes[player_path[i + 1]]

        pygame.draw.line(screen, PATH, start_pos, end_pos, 8)
        pygame.draw.line(screen, (255, 230, 180), start_pos, end_pos, 2)

    #draw nodes
    for node, pos in nodes.items():
        color = NORMAL

        if node in level.get("keys", []):
            color = GOLD
        elif node in level.get("traps", []):
            color = EMBER
        elif node in level.get("treasures", []):
            color = (255, 215, 0)

        if node == level["start"]:
            color = MOSS
        elif node == level["end"]:
            color = BLOOD

        pygame.draw.circle(screen, (255, 255, 255), pos, 42, 2)
        pygame.draw.circle(screen, color, pos, 35)
        pygame.draw.circle(screen, BRONZE, pos, 35, 3)

        txt = font.render(str(node), True, PARCHMENT)
        screen.blit(txt, (pos[0] - 10, pos[1] - 12))

   #HUD
    pygame.draw.rect(screen, STONE, (15, 15, 980, 90), border_radius=15)
    pygame.draw.rect(screen, BRONZE, (15, 15, 980, 90), 3, border_radius=15)

    hud = font.render(
        f"Chamber {level_index + 1}: {level['name']} | Treasure: {score} | Path Cost: {player_weight} | Key: {'Yes' if has_key else 'No'}",
        True,
        PARCHMENT
    )
    screen.blit(hud, (30, 25))

    #instructions = small_font.render(
    #    "Gold = Key | Orange = Trap | Bright Gold = Treasure",
    #    True,
    #    (200, 200, 200)
    #)
    # screen.blit(instructions, (30, 60))

   #finish screen
    if game_state == "FINISHED":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

    
        victory = font.render("Door Unlocked!", True, GOLD)
        screen.blit(victory, (WIDTH // 2 - victory.get_width() // 2, HEIGHT // 2 - 140))

        distances, prev = dijkstra(graph, level["start"])
        best_weight = distances[level["end"]]
        difference = player_weight - best_weight

        if difference == 0:
            stars = 3
        elif difference <= 3:
            stars = 2
        else:
            stars = 1

        win_text = big_font.render("CHAMBER CLEARED", True, GOLD)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 200))    
        
        #score display
        result = font.render(
            f"Optimal Weight: {best_weight}", True, PARCHMENT
        )
        screen.blit(result, (WIDTH // 2 - result.get_width() // 2, HEIGHT // 2 - 60))

        #user attempt
        your_run = font.render(f"Your Path Cost: {player_weight}", True, EMBER)
        screen.blit(your_run, (WIDTH // 2 - your_run.get_width() // 2, HEIGHT // 2 - 20))
       
        #best path
        best_path = reconstruct_path(prev, level["start"], level["end"])
        best_path_text = small_font.render(
            f"Best Path: {' -> '.join(best_path)}", True, PARCHMENT
        )
        screen.blit(best_path_text, (WIDTH // 2 - best_path_text.get_width() // 2, HEIGHT // 2 + 20))

        #star stuff
        start_x = WIDTH // 2 - 80
        y = HEIGHT // 2 + 100

        #draw stars for results
        for i in range(3):
            if i < stars:
                size = int(18 * pulse)
                draw_star(screen, GOLD, (start_x + i * 70, y), 18, glow=True)
            else:
                size = 15
                draw_star(screen, (80, 70, 60), (start_x + i * 70, y), 18)
        
        # continue to next level
        next_level = small_font.render(
            "Press SPACE to continue", True, GOLD
        )
        screen.blit(next_level, (WIDTH // 2 - next_level.get_width() // 2, HEIGHT // 2 + 160))

    if game_state == "GAME_OVER":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))

    # title
        title = big_font.render("DUNGEON CLEARED", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))

        # score
        score_text = font.render(f"Final Treasure: {score}", True, PARCHMENT)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))

        # good job
        msg = small_font.render("You mastered Dijkstra’s Algorithm.", True, GOLD)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 10))

        # restart control
        restart = small_font.render("Press SPACE to return to menu", True, (200, 200, 200))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 80))        
  
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
            clicked = get_clicked_node(pygame.mouse.get_pos(), nodes)

            if clicked:
                current = player_path[-1]
                
                #undo player move
                if len(player_path) > 1 and clicked == player_path[-2]:
                    last_node = player_path.pop()
                    removed_weight = valid_move(graph, clicked, last_node)

                    if removed_weight:
                        player_weight -= removed_weight

                else:
                    weight = valid_move(graph, current, clicked)

                    if weight:
                        player_path.append(clicked)
                        player_weight += weight

                        # hidden stuff
                        if clicked in level.get("keys", []):
                            has_key = True

                        if clicked in level.get("traps", []):
                            player_weight += 5

                        if clicked in level.get("treasures", []) and clicked not in collected_treasures:
                            score += 25
                            collected_treasures.add(clicked)

                        # 
                        if clicked == level["end"]:
                            if level.get("keys") and not has_key:
                                player_path.pop()
                                player_weight -= weight
                                continue

                            game_state = "FINISHED"
                            distances, _ = dijkstra(graph, level["start"])
                            best_weight = distances[level["end"]]

                            score += max(
                                10,
                                100 - (player_weight - best_weight) * 10
                            )
        #                  
        if event.type == pygame.KEYDOWN:
            if game_state == "FINISHED":
                if event.key == pygame.K_SPACE:
                    level_index += 1

                    if level_index >= len(levels):
                        game_state = "GAME_OVER"
                    else:
                        level, player_path, player_weight, finished, has_key, collected_treasures = load_level(level_index)
                        game_state = "PLAYING"

            elif game_state =="GAME_OVER":
                if event.key ==pygame.K_SPACE: # go to menu
                    if not show_menu(screen, WIDTH, HEIGHT):
                        running = False
                    else:
                        level_index = 0
                        score = 0
                        level, player_path, player_weight, finished, has_key, collected_treasures = load_level(level_index)
                        game_state = "PLAYING"

    pygame.display.flip()
clock.tick(60)

pygame.quit()