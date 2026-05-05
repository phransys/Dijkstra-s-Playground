# menu.py
import pygame

# Dungeon Palette
BG = (28, 24, 20)
STONE = (55, 48, 42)
BRONZE = (120, 90, 50)
GOLD = (190, 150, 70)
EMBER = (220, 120, 40)
PARCHMENT = (220, 210, 180)


def draw_button(screen, rect, text, font, mouse_pos):
    color = (70, 55, 40)

    if rect.collidepoint(mouse_pos):
        color = (110, 80, 50)

    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BRONZE, rect, 3, border_radius=12)

    txt = font.render(text, True, PARCHMENT)
    screen.blit(
        txt,
        (
            rect.x + rect.width // 2 - txt.get_width() // 2,
            rect.y + rect.height // 2 - txt.get_height() // 2
        )
    )


def show_menu(screen, WIDTH, HEIGHT):
    title_font = pygame.font.SysFont("georgia", 60, bold=True)
    button_font = pygame.font.SysFont("consolas", 28, bold=True)
    small_font = pygame.font.SysFont("consolas", 22)

    clock = pygame.time.Clock()

    start_button = pygame.Rect(WIDTH // 2 - 140, 360, 280, 75)
    quit_button = pygame.Rect(WIDTH // 2 - 140, 470, 280, 75)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(BG)

        # Stone floor pattern
        for x in range(0, WIDTH, 80):
            for y in range(0, HEIGHT, 80):
                pygame.draw.rect(screen, STONE, (x, y, 78, 78), 1)

        # Torches
        pygame.draw.circle(screen, EMBER, (80, 150), 28)
        pygame.draw.circle(screen, (255, 180, 80), (80, 150), 14)

        pygame.draw.circle(screen, EMBER, (WIDTH - 80, 150), 28)
        pygame.draw.circle(screen, (255, 180, 80), (WIDTH - 80, 150), 14)

        # Title
        title = title_font.render("Dijkstra's Playground", True, GOLD)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        subtitle = small_font.render(
            "Escape the Dungeon by Finding the Shortest Path",
            True,
            PARCHMENT
        )
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 210))

        draw_button(screen, start_button, "Start Adventure", button_font, mouse_pos)
        draw_button(screen, quit_button, "Leave Dungeon", button_font, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return True

                if quit_button.collidepoint(mouse_pos):
                    return False

        clock.tick(60)