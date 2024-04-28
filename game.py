import sys
import pygame

from scripts.settings import *
from scripts.level import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project Dango Version2")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick() / 1000
            self.level.update(dt)
            self.level.render(dt)
                    
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()