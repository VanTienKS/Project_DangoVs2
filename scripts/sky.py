import pygame
from random import randint, choice
from scripts.settings import *
from scripts.supports import *
from scripts.sprites import Generic

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.start_color = [255,255,255]
        self.end_color = (38,101,189)
        
    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt
                
        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

class Drop(Generic):
    def __init__(self, pos, surf, moving, groups, z):
        # general setup
        super().__init__(pos, surf, groups, z)
        
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # moving
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, map_name, all_sprite):
        self.all_sprites = all_sprite
        self.rain_drops = import_folder('graphics/rain/drops/')
        self.rain_floor = import_folder('graphics/rain/floor/')
        # self.floor_w, self.floor_h = pygame.image.load(f'graphics/world/{map_name}.png').get_size()
        self.floor_w, self.floor_h = SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2
        
    def create_floor(self):
        Drop(
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            surf=choice(self.rain_floor),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor']
        )

    def create_drops(self):
        Drop(
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            surf=choice(self.rain_drops),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain floor']
        )

    def update(self):
        self.create_floor()
        self.create_drops()
