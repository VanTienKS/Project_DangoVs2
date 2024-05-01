import pygame
from scripts.settings import *
from scripts.supports import *
from scripts.timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, name, pos, status, item_inventory, seed_inventory, group, collision_sprites, tree_sprites, interaction_sprites, soil_layer, toggle_shop, toggle_chat):
        super().__init__(group)

        # general setup
        self.name = name
        self.import_assets()
        self.status = status
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites
        
        # interaction
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction_sprites
        self.soil_layer = soil_layer
        self.sleep = False
        self.toggle_shop = toggle_shop
        self.toggle_chat = toggle_chat

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        
        # inventory
        self.item_inventory = item_inventory
        
        self.seed_inventory = seed_inventory
        self.money = 200

        # timer
        self.timers = {
            'tool use': Timer(500 * len(self.animations[self.status]), self.use_tool),
            'tool switch': Timer(1000),
            'seed use': Timer(300, self.use_seed),
            'seed switch': Timer(800),
            'interaction': Timer(500)
        }

        # movement setup
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 500
        
        # sound
        self.watering = pygame.mixer.Sound('audio/water.mp3')
        self.watering.set_volume(0.1)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
                           'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                           'up_water': [], 'down_water': [], 'left_water': [], 'right_water': [],
                           }
        base_path = 'graphics/character/'
        for animation in self.animations.keys():
            full_path = base_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        if self.selected_tool in self.status:
            self.frame_index = min(
                self.frame_index + (2 * dt), len(self.animations[self.status]) - (2 * dt))
            if self.frame_index >= len(self.animations[self.status]):
                self.status = self.status.replace(self.selected_tool, 'idle')
        else:
            self.frame_index = (self.frame_index + (2 * dt)
                                ) % len(self.animations[self.status])
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        # if we don't use tool then we can move
        if not self.timers['tool use'].active and not self.sleep:
            self.direction.x, self.status = (-1, 'left') if keys[pygame.K_LEFT] else (
                (1, 'right') if keys[pygame.K_RIGHT] else (0, self.status))
            self.direction.y, self.status = (-1, 'up') if keys[pygame.K_UP] else (
                (1, 'down') if keys[pygame.K_DOWN] else (0, self.status))

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]

        # seed use
        if keys[pygame.K_a] and not self.timers['seed use'].active:
            print('avc')
            self.timers['seed use'].activate()
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # change seed
        if keys[pygame.K_e] and not self.timers['seed switch'].active:
            self.timers['seed switch'].activate()
            self.seed_index = (self.seed_index + 1) % len(self.seeds)
            self.selected_seed = self.seeds[self.seed_index]
            
        if keys[pygame.K_RETURN]:
            vacham = False
            for sprite in self.interaction_sprites.sprites():
                if hasattr(sprite, 'hitbox'):
                    if sprite.rect.colliderect(self.hitbox):
                        vacham = True
                        if not self.timers['interaction'].active:
                            self.timers['interaction'].activate()
                            if sprite.name == 'Trader':
                                self.toggle_shop()
                                self.status = self.status.split('_')[0] + '_idle'
                            elif sprite.name == 'Bed':
                                self.sleep = not self.sleep
                                self.pos = Vector2(sprite.rect.topright if not self.sleep else sprite.rect.topleft, sprite.rect[1] + 10)
                                
                                self.status = 'down_idle' if self.sleep else 'right_idle'
            if not vacham:
                self.timers['interaction'].activate()
                self.toggle_chat()
                self.status = self.status.split('_')[0] + '_idle'
            self.direction = pygame.math.Vector2()
            
            # collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction_sprites, False)
            # if collided_interaction_sprite:
            #     if not self.timers['interaction'].active:
            #         self.timers['interaction'].activate()
            #         if collided_interaction_sprite[0].name == 'Trader':
            #             self.toggle_shop()
            #             self.status = self.status.split('_')[0] + '_idle'
            #         elif collided_interaction_sprite[0].name == 'Bed':
            #             self.sleep = not self.sleep
            #             self.pos = Vector2(collided_interaction_sprite[0].rect.topright if not self.sleep else collided_interaction_sprite[0].rect.topleft, collided_interaction_sprite[0].rect[1] + 10)
                        
            #             self.status = 'down_idle' if self.sleep else 'right_idle'
            # else:
            #     self.timers['interaction'].activate()
            #     self.toggle_chat()
            #     self.status = self.status.split('_')[0] + '_idle'
            # self.direction = pygame.math.Vector2()
            
    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        elif self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.hitbox.collidepoint(self.target_pos):
                    tree.damage(self)
        elif self.selected_tool == 'water':
            self.watering.play()
            self.soil_layer.water(self.target_pos)

    def use_seed(self):
        print(self.selected_seed)
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            self.seed_inventory[self.selected_seed] -= 1

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction[0] > 0:  # move right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction[0] < 0:  # move left
                            self.hitbox.left = sprite.hitbox.right

                        self.pos.x = self.hitbox.centerx
                        self.rect.centerx = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction[1] > 0:  # move down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction[1] < 0:  # move up
                            self.hitbox.top = sprite.hitbox.bottom

                        self.pos.y = self.hitbox.centery
                        self.rect.centery = self.hitbox.centery

    def move(self, dt):

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        # self.hitbox.centerx = round(self.pos.x)
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        # self.hitbox.centery = round(self.pos.y)
        self.hitbox.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt, canMove=True):
        if canMove:
            self.input()
            self.get_status()

        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)

