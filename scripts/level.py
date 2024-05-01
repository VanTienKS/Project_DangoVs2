import pygame


from random import randint
from scripts.settings import *
from scripts.supports import *
from scripts.sprites import *
from scripts.network import Network
from scripts.overlay import Overlay
from scripts.player import Player
from scripts.transition import Transition
from scripts.soil import SoilLayer
from scripts.sky import Rain, Sky
from scripts.menu import Menu
from scripts.chat1 import Chat

from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self):
        # network
        self.network = Network()

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # sky
        self.sky = Sky()
        
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player1)
        self.transition = Transition(self.reset, self.player1, self.player2)

        self.rain = Rain(self.all_sprites)
        # self.raining = randint(0,20) > 15
        self.soil_layer.raining = self.raining
        
        # sounds
        self.success = pygame.mixer.Sound('audio/success.wav')
        self.success.set_volume(0.1)
        self.music = pygame.mixer.Sound('audio/bg.mp3')
        self.music.set_volume(0.2)
        # self.music.play(loops = -1)


        # shop
        self.menu = Menu(self.player1, self.toggle_shop)
        self.shop_active = False
        
        self.error_frameP2 = 0
        self.new_day = False

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')
        
        # Water 
        for x, y, _ in tmx_data.get_layer_by_name('Water').tiles():
            Water((x*TILE_SIZE, y*TILE_SIZE), import_folder('graphics/water'), self.all_sprites)

        # Ground
        for x, y, surf in tmx_data.get_layer_by_name('Ground').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        # Forest Grass
        for x, y, surf in tmx_data.get_layer_by_name('Forest Grass').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['soil'])

        # Soil
        for x, y, surf in tmx_data.get_layer_by_name('Outside Decoration').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground plant'])

        # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
                
        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites)
                
        # Hill
        for x, y, surf in tmx_data.get_layer_by_name('Hills').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites], LAYERS['ground plant'])   
                         
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])   
            
        # Decoration
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])     
        
        # Tree
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name, self.player_add)    
        
        # Collision    
        for obj in tmx_data.get_layer_by_name('Collisions'):
            Collision((obj.x, obj.y), obj.width, obj.height, [self.collision_sprites])
        
        # Object
        for obj in tmx_data.get_layer_by_name('Objects'):
            Generic((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])     

        # Interaction with Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Bed':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)   
        
        fullInfo = self.network.getInfo()
        
        self.player1 = Player(fullInfo['player1']['name'], fullInfo['player1']
                              ['pos'], fullInfo['player1']['status'], fullInfo['player1']['item_inventory'], fullInfo['player1']['seed_inventory'], self.all_sprites, self.collision_sprites, self.tree_sprites, self.interaction_sprites, self.soil_layer, self.toggle_shop, self.toggle_chat)
        self.player2 = Player(fullInfo['player2']['name'], fullInfo['player2']
                              ['pos'], fullInfo['player2']['status'], fullInfo['player2']['item_inventory'], fullInfo['player2']['seed_inventory'], self.all_sprites, self.collision_sprites, self.tree_sprites, self.interaction_sprites, self.soil_layer, self.toggle_shop, self.toggle_chat)
        self.sky.start_color = fullInfo['start_color']
        self.raining = fullInfo['rain']
        
        # chat
        self.chat = Chat(self.player1.name, self.toggle_chat)
        self.chat_active = False
        self.chat.output_text_lines = fullInfo['chat']
        
    def toggle_shop(self):
        self.shop_active = not self.shop_active  

    def toggle_chat(self):
        self.chat_active = not self.chat_active    

    def player_add(self, player, item):
        player.item_inventory[item] += 1
        self.success.play()

    def reset(self):
        self.new_day = True
        # plants
        self.soil_layer.update_plants()
        # soil
        self.soil_layer.remove_water()
        self.raining = randint(0,20) > 10
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()
        
        # apples on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()
            
        # sky
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player1.hitbox):
                    self.player_add(self.player1, plant.plant_type)
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
                    plant.kill()
                if plant.harvestable and plant.rect.colliderect(self.player2.hitbox):
                    self.player_add(self.player2, plant.plant_type)
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
                    plant.kill()

    def send_and_recv_data(self):

        output_text_lines = []
        if self.chat.has_chat:
            self.chat.has_chat = False
            output_text_lines = self.chat.output_text_lines
        rain = None
        if self.new_day:
            self.new_day = False
            rain = self.raining
        
        send_Info = {
            'player1': {
                'name': self.player1.name,
                'pos': self.player1.pos,
                'status': self.player1.status,
                'frame_index': self.player1.frame_index,
                'selected_tool': self.player1.selected_tool,
                'selected_seed': self.player1.selected_seed,
                'item_inventory':self.player1.item_inventory,
                'seed_inventory':self.player1.seed_inventory,
                'sleep': self.player1.sleep,
            },
            'start_color': self.sky.start_color,
            'chat': output_text_lines,
            'rain': rain,
        }
        recvInfo = self.network.send(send_Info)

        self.player2.pos = recvInfo['player2']['pos']
        if self.player2.status != recvInfo['player2']['status'] and len(recvInfo['player2']['status'].split('_')) > 1:
            if recvInfo['player2']['status'].split('_')[1] in self.player2.tools:
                self.player2.timers['tool use'].activate()
            if recvInfo['player2']['status'].split('_')[1] in self.player2.seeds:
                self.player2.timers['seed use'].activate()
        
        self.player2.status = recvInfo['player2']['status']
        self.player2.frame_index = recvInfo['player2']['frame_index'] if recvInfo[
            'player2']['frame_index'] != self.error_frameP2 else self.player2.frame_index
        
        self.player2.selected_tool = recvInfo['player2']['selected_tool']
        self.player2.selected_seed = recvInfo['player2']['selected_seed']
        self.player2.item_inventory = recvInfo['player2']['item_inventory']
        self.player2.seed_inventory = recvInfo['player2']['seed_inventory']
        
        if 100 < self.transition.color < 255 and recvInfo['player2']['sleep'] == False:
            self.transition.color = 255
            self.transition.speed = -2
            self.player1.sleep = False
            self.player1.pos.x += 150
        self.player2.sleep = recvInfo['player2']['sleep']

         
        self.sky.start_color = recvInfo['start_color']
        self.chat.output_text_lines = recvInfo['chat']
        self.raining = recvInfo['rain']
        

        self.error_frameP2 = recvInfo['player2']['frame_index']

    def update(self, dt):
        for sprite in self.all_sprites.sprites():
            if sprite is self.player2 or (sprite is self.player1 and self.shop_active) or (sprite is self.player1 and self.chat_active):
                sprite.update(dt, canMove=False)
            # elif sprite is self.player1 and not self.shop_active:
            #     sprite.update(dt)
            else:
                sprite.update(dt)
        self.plant_collision()        
        self.send_and_recv_data()
        print(self.raining)

    def render(self, dt):
        # drawing logic
        self.display_surface.fill((0, 0, 0))
        self.all_sprites.customize_draw(self.player1, self.player2)
        
        # weather
        if self.raining:
            self.rain.update()
        # overlay
        self.overlay.display()
        # day time
        self.sky.display(dt)
        
        # shopping
        if self.shop_active:
            self.menu.display()
        
        # chating
        if self.chat_active:
            self.chat.update()
            
        # transition overlay
        if self.player1.sleep and self.player2.sleep:
            self.transition.play()  
    
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def in_screen(self, sprite, player):
        if player.rect.centerx - (SCREEN_WIDTH/2 + player.rect.width) < sprite.rect.centerx < player.rect.centerx +  (SCREEN_WIDTH/2 + player.rect.width):
            if player.rect.centery - (SCREEN_HEIGHT/2 + player.rect.height) < sprite.rect.centery < player.rect.centery + (SCREEN_HEIGHT/2 + player.rect.height):
                return True
        return False

    def customize_draw(self, player1, player2):
        self.offset.x = player1.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player1.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    if self.in_screen(sprite, player1):
                        offset_rect = sprite.rect.copy()
                        offset_rect.center -= self.offset
                        self.display_surface.blit(sprite.image, offset_rect)
                        # if isinstance(sprite, Player) or isinstance(sprite, Tree):
                        #     pygame.draw.rect(self.display_surface, (0,255,0), offset_rect, 5)
                        #     hitbox_rect = sprite.hitbox.copy()
                        #     hitbox_rect.center = offset_rect.center
                        #     pygame.draw.rect(self.display_surface, 'gray', hitbox_rect, 5)
                        # if isinstance(sprite, Player):  
                        #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[sprite.status.split('_')[0]]
                        #     pygame.draw.circle(self.display_surface, (0,0,200), target_pos, 5)

        debug(self.display_surface, player1.name, (player1.rect.centerx -
              self.offset.x, player1.rect.centery - self.offset.y - 40), (255, 255, 0))
        debug(self.display_surface, player2.name, (player2.rect.centerx -
              self.offset.x, player2.rect.centery - self.offset.y - 40), (0, 200, 200))
