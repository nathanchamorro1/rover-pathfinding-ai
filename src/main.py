import pygame
from config import *
from grid import create_grid
from astar import a_star_animated

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rover A* Path Planner")
clock = pygame.time.Clock()  # For controlling animation speed

grid = create_grid()
start = None
goal = None
running = True
path = []
explored = set()
searching = False
search_generator = None

def draw_everything():
    """Helper function to draw the grid"""
    screen.fill(WHITE)
    
    for row in grid:
        for cell in row:
            cell.draw(screen)
    
    for c in explored:
        pygame.draw.rect(screen, BLUE, (c.x, c.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)
    
    if path:
        for c in path:
            pygame.draw.rect(screen, YELLOW, (c.x, c.y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)
    
    if start:
        pygame.draw.rect(screen, GREEN, (start.x, start.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (start.x, start.y, CELL_SIZE, CELL_SIZE), 1)
    
    if goal:
        pygame.draw.rect(screen, RED, (goal.x, goal.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (goal.x, goal.y, CELL_SIZE, CELL_SIZE), 1)
    
    pygame.display.flip()

while running:
    clock.tick(60)  # 60 FPS
    
    # If we're searching, advance the algorithm one step
    if searching and search_generator:
        try:
            current, explored, result_path = next(search_generator)
            if result_path is not None:  # Found path!
                path = result_path
                searching = False
                print("Path found!")
            elif current is None:  # No path
                path = []
                searching = False
                print("Oops! No path was found.")
        except StopIteration:
            searching = False
    
    draw_everything()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if pygame.mouse.get_pressed()[0] and not searching:  # Can't draw while searching
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

pygame.quit()


# import pygame
# from config import *
# from grid import create_grid
# from astar import a_star

# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Rover A* Path Planner")

# grid = create_grid()
# start = None
# goal = None

# running = True
# path = []
# explored = set()

# while running:
#     screen.fill(WHITE)

#     for row in grid:
#         for cell in row:
#             cell.draw(screen)

#     for c in explored:
#         pygame.draw.rect(screen, BLUE, (c.x, c.y, CELL_SIZE, CELL_SIZE))
#         pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)
    
#     if path: # since there might be no path returned
#         for c in path:
#             pygame.draw.rect(screen, GREEN, (c.x, c.y, CELL_SIZE, CELL_SIZE))
#             pygame.draw.rect(screen, GRAY, (c.x, c.y, CELL_SIZE, CELL_SIZE), 1)

#     if start:
#         pygame.draw.rect(screen, GREEN, (start.x, start.y, CELL_SIZE, CELL_SIZE))
#         pygame.draw.rect(screen, GRAY, (start.x, start.y, CELL_SIZE, CELL_SIZE), 1)
    
#     if goal:
#         pygame.draw.rect(screen, RED, (goal.x, goal.y, CELL_SIZE, CELL_SIZE))
#         pygame.draw.rect(screen, GRAY, (goal.x, goal.y, CELL_SIZE, CELL_SIZE), 1)

#     pygame.display.flip() # updates entire screen display

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
        
#         if pygame.mouse.get_pressed()[0]:
#             x, y = pygame.mouse.get_pos()
#             r = y // CELL_SIZE
#             c = x // CELL_SIZE
#             if 0 <= r < ROWS and 0 <= c < COLS:
#                 grid[r][c].is_obstacle = True
        
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_s: # press s to set start
#                 x, y = pygame.mouse.get_pos()
#                 r, c = y // CELL_SIZE , x // CELL_SIZE
#                 if 0 <= r < ROWS and 0 <= c < COLS:
#                     if start:
#                         start.is_start = False
#                     start = grid[r][c]
#                     start.is_start = True
            
#             if event.key == pygame.K_g: # press g to set goal
#                 x, y = pygame.mouse.get_pos()
#                 r, c = y // CELL_SIZE , x // CELL_SIZE
#                 if 0 <= r < ROWS and 0<= c < COLS:
#                     if goal:
#                         goal.is_goal = False
#                     goal = grid[r][c]
#                     grid[r][c].is_goal = True
            
#             if event.key == pygame.K_SPACE:
#                 if start and goal:
#                     result_path, explored = a_star(start, goal, grid)
#                     if result_path:
#                         path = result_path
#                     else:
#                         path = []
#                         print('Oops! No path was found.')

#             if event.key == pygame.K_r:
#                 grid = create_grid()
#                 start = None
#                 goal = None
#                 path = []
#                 explored = set()
# pygame.quit()
