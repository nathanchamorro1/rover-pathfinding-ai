# rover.py
import pygame
from config import CELL_SIZE

class Rover:
    def __init__(self, path):
        self.step_frames = 10  # frames per grid step
        self.reset(path)

        # Load, scale rover image
        self.image = pygame.image.load("assets/rover.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def reset(self, path):
        self.path = path or []
        self.index = 0
        self.finished = False
        self.frame_counter = 0

    @property
    def cell(self):
        if not self.path:
            return None
        return self.path[self.index]

    def update(self):
        if self.finished or not self.path:
            return

        self.frame_counter += 1
        if self.frame_counter >= self.step_frames:
            self.frame_counter = 0
            if self.index < len(self.path) - 1:
                self.index += 1
            else:
                self.finished = True

    def draw(self, screen):
        c = self.cell
        if not c:
            return

        # Draw rover image directly on the cell
        screen.blit(self.image, (c.x, c.y))