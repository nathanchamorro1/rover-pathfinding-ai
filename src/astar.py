from heapq import heappush, heappop
from config import *

# manhattan distance (like walking)
def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def get_neighbors(cell, grid):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dr, dc in dirs:
        r, c = cell.row + dr, cell.col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if not grid[r][c].is_obstacle:
                neighbors.append(grid[r][c])
    return neighbors

def a_star_animated(start, goal, grid):
    open_set = []
    counter = 0
    heappush(open_set, (0, counter, start))
    
    birthed_from = {}
    g_score = {start: 0}
    explored = set()
    
    while open_set:
        _, _, current = heappop(open_set)
        
        if current in explored:
            continue
            
        explored.add(current)
        yield current, explored, None  # Yield progress: (current_cell, explored_set, path)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in birthed_from:
                path.append(current)
                current = birthed_from[current]
            path.reverse()
            yield None, explored, path  # Yield final result
            return
        
        for neighbor in get_neighbors(current, grid):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                birthed_from[neighbor] = current
                g_score[neighbor] = temp_g
                f = temp_g + heuristic(neighbor, goal)
                counter += 1
                heappush(open_set, (f, counter, neighbor))
    
    yield None, explored, None  # No path found

# Keep the old function for backwards compatibility
def a_star(start, goal, grid):
    """Non-animated version - runs instantly"""
    for current, explored, path in a_star_animated(start, goal, grid):
        if path is not None or (current is None and path is None):
            return path, explored
    return None, explored

# from heapq import heappush, heappop
# from config import *

# # manhattan distance (like walking)
# def heuristic(a, b):
#     return abs(a.row - b.row) + abs(a.col - b.col)

# def get_neighbors(cell, grid):
#     dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)] # only moving down, up, right, left NO DIAGNOL
#     neighbors = []

#     for dr, dc in dirs:
#         r, c = cell.row + dr, cell.col + dc
#         if 0 <= r < ROWS and 0 <= c < COLS:
#             if not grid[r][c].is_obstacle:
#                 neighbors.append(grid[r][c])

#     return neighbors

# def a_star(start, goal, grid):
#     open_set = []
#     counter = 0 # in case the estimated total cost is the same for more than one node
#     heappush(open_set, (0, counter, start))

#     birthed_from = {}

#     g_score = {start:0} # distance from start
#     f_score = {start: heuristic(start, goal)} # estimated total cost

#     explored = set() # no duplicates

#     while open_set:
#         _, _, current = heappop(open_set)
#         if current == goal:
#             path = []
#             while current in birthed_from:
#                 path.append(current)
#                 current = birthed_from[current]
#             path.reverse() # reconstructed the path backwards initially
#             return path, explored
        
#         explored.add(current)

#         for neighbor in get_neighbors(current, grid):
#             temp_g = g_score[current] + 1
#             if neighbor not in g_score or temp_g < g_score[neighbor]:
#                 birthed_from[neighbor] = current
#                 g_score[neighbor] = temp_g
#                 f = temp_g + heuristic(neighbor, goal)
#                 f_score[neighbor] = f
#                 counter += 1
#                 heappush(open_set, (f, counter, neighbor))

#     return None, explored # in case there is no path