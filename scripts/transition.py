import pygame
from scripts.settings import *


class Transition:
    def __init__(self, reset, player1, player2):

        # set up
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player1 = player1
        self.player2 = player2

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self):
        # 1. call reset
        # 2. wake up the player
        # 3. set the speed to -2 at the end of the transition
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:    
            self.color = 255
            self.speed = -2
            self.player1.sleep = False
            self.player1.pos.x += 150
            
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
