import pygame
from config import *
from grid import create_grid
from astar import a_star_animated
import rover as rover_module

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rover A* Path Planner")
clock = pygame.time.Clock()

grid = create_grid()
start = None
goal = None
running = True
path = []
explored = set()
searching = False
search_generator = None
rover = None
popup_message = None
popup_timer = 0


def draw_everything():
    screen.fill(WHITE)  # background

    # draw grid cells
    for row in grid:
        for cell in row:
            cell.draw(screen)

    # explored cells in blue
    for c in explored:
        pygame.draw.rect(screen, BLUE, (c.x, c.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)

    # path in yellow
    if path:
        for c in path:
            pygame.draw.rect(screen, YELLOW, (c.x, c.y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)

    # start and goal on top
    if start:
        pygame.draw.rect(screen, GREEN, (start.x, start.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (start.x, start.y, CELL_SIZE, CELL_SIZE), 1)

    if goal:
        pygame.draw.rect(screen, RED, (goal.x, goal.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (goal.x, goal.y, CELL_SIZE, CELL_SIZE), 1)

    # rover on top of everything
    if rover:
        rover.draw(screen)

    draw_popup()

    pygame.display.flip()

def draw_popup():
    if not popup_message:
        return

    # dark transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # popup box
    box_width = 250
    box_height = 100
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2, border_radius=10)

    # text
    font = pygame.font.SysFont(None, 28)
    text = font.render(popup_message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

while running:
    clock.tick(60)

    # step A* animation
    if searching and search_generator:
        try:
            current, explored, result_path = next(search_generator)
            if result_path is not None:  # found path
                path = result_path
                searching = False
                print("Path found!")
                if path:
                    rover = rover_module.Rover(path)
            elif current is None:  # no path
                path = []
                searching = False
                popup_message = "Oops! No path was found"
                popup_timer = 120
        except StopIteration:
            searching = False


    if rover and not searching:
        rover.update()

    if popup_timer > 0:
        popup_timer -= 1
    if popup_timer == 0:
            popup_message = None

    draw_everything()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0] and not searching:
            x, y = pygame.mouse.get_pos()
            r = y // CELL_SIZE
            c = x // CELL_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r][c].is_obstacle = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not searching:
                x, y = pygame.mouse.get_pos()
                r, c = y // CELL_SIZE, x // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if start:
                        start.is_start = False
                    start = grid[r][c]
                    start.is_start = True


            if event.key == pygame.K_g and not searching:
                x, y = pygame.mouse.get_pos()
                r, c = y // CELL_SIZE, x // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if goal:
                        goal.is_goal = False
                    goal = grid[r][c]
                    goal.is_goal = True

            if event.key == pygame.K_SPACE and not searching:
                if start and goal:
                    path = []
                    explored = set()
                    rover = None
                    search_generator = a_star_animated(start, goal, grid)
                    searching = True

            if event.key == pygame.K_r:
                grid = create_grid()
                start = None
                goal = None
                path = []
                explored = set()
                searching = False
                search_generator = None
                rover = None

pygame.quit()