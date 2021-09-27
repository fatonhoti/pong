from game_object import GameObject
from settings import *
import pygame

class Paddle(GameObject):

    def __init__(self, x, y):
        super(Paddle,self).__init__(
            x,
            y,
            0,
            0
        )
    
    def draw(self, screen):
        figure = pygame.Rect(
            self.x, 
            self.y, 
            PADDLE_WIDTH, 
            PADDLE_HEIGHT
        )
        pygame.draw.rect(screen, WHITE, figure)
