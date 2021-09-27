from random import choice

import pygame

from game_object import GameObject
from settings import *


class Ball(GameObject):
    def __init__(self):
        super(Ball, self).__init__(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            dx=MAX_BALL_SPEED * choice((-1, 1)),
            dy=MAX_BALL_SPEED * choice((-1, 1)),
        )

    def draw(self, screen):
        figure = pygame.Rect(self.x, self.y, BALL_RADIUS, BALL_RADIUS)
        pygame.draw.ellipse(screen, WHITE, figure)

    def reset(self, screen):
        figure = pygame.Rect(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS
        )
        pygame.draw.ellipse(screen, WHITE, figure)
