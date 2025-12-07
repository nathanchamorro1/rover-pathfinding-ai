from config import *
import pygame

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.is_obstacle = False
        self.is_start = False
        self.is_goal = False

    def draw(self, screen):
        color = WHITE
        if self.is_obstacle:
            color = BLACK
        elif self.is_start:
            color = GREEN
        elif self.is_goal:
            color = RED
        
        pygame.draw.rect(screen, color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GRAY, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)


def create_grid():
    return [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]