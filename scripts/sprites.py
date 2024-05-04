import pygame
from scripts.settings import *
from scripts.supports import *
from scripts.timer import Timer
from random import randint, choice

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z 
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.3 , -self.rect.height * 0.3)
     
class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        self.name = name
        super().__init__(pos, surf, groups)
        
class Water(Generic):
    def __init__(self, pos, frames, groups):
        # animation setup
        self.frames = frames
        self.frame_index = 0
        
        # sprite setup
        super().__init__(pos, self.frames[self.frame_index], groups, LAYERS['water'])
    
    def update(self, dt):
        self.frame_index = (self.frame_index + (2 * dt)) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]
        
class WildFlower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.7) 
 
class Particle(Generic):
    def __init__(self, pos, surface, groups, z, duration = 200):
        super().__init__(pos, surface, groups, z = z)
        
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        
        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf
        
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()
            
class Tree(Generic):
    def __init__(self, pos, surface, groups, name, player_add):
        
        self.all_sprites = groups[0]
        self.player_add = player_add
        
        # tree attributes
        self.health = 5
        self.alived = True
        self.stump_surf = import_image(f'graphics/stumps/{'small' if name == 'Small' else 'large'}.png')
        self.invul_timer = Timer(200)
        
        # apples
        self.apples_surf = import_image('graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        
        super().__init__(pos, surface, groups)
        self.create_fruit()
        
        # sounds
        self.axe_sound = pygame.mixer.Sound('audio/axe.mp3')
        
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x, y), self.apples_surf, [self.all_sprites, self.apple_sprites], z = LAYERS['fruit'])
    
    def damage(self, player):
        # damaging the tree
        self.health -= 1
        
        # play sound
        self.axe_sound.play()
        if self.health <= 0:
            self.player_add(player, 'wood')
        
        # remove an apple
        if len(self.apple_sprites.sprites()):
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image, self.all_sprites, LAYERS['fruit'])
            self.player_add(player, 'apple')
            random_apple.kill()
            
    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruit'], 500)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alived = False    
            
    def update(self, dt):
        if self.alived:
            self.check_death()            
               
        
class Collision(Generic):
    def __init__(self, pos, size, groups):
        
        surface = pygame.Surface(size)
        surface.fill('red')
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy()