import pygame 
from util import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from soil import *
from transition import Transition
from menu import Menu
from help import *

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites)
        self.interaction_sprites = pygame.sprite.Group()
        
        self.toggles = [self.toggle_menu, self.toggle_info, self.toggle_credits]

          
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False
        
        self.menus = [HelpMenu(self.toggles[MENUS['help']]), GameInfo(self.toggles[MENUS['info']]), CreditMenu(self.toggles[MENUS['credits']])]
        self.menuactives = [False, False, False]
        
        self.success = pygame.mixer.Sound('audio/success.wav')
        self.success.set_volume(0.2)
        
        self.music = pygame.mixer.Sound('audio/music.m4a')
        self.music.set_volume(0.5)
        self.music.play(loops=-1)
        
    
    def setup(self):
        tmx = load_pygame('field.tmx')

        for layer in ['houseground', 'housewall']:
            for x, y, tilesurface in tmx.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), tilesurface, self.all_sprites, LAYERS['house bottom'])
   
        for layer in ['housefurniture', 'housedecor']:
            for x, y, tilesurface in tmx.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), tilesurface, [self.all_sprites], LAYERS['house bottom'])
   
        for layer in ['fences']:
            for x, y, tilesurface in tmx.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), tilesurface, [self.all_sprites])

        # for layer in ['vegtrees']:
        # 	for x, y, tilesurface in tmx.get_layer_by_name(layer).tiles():
        # 		Generic((x*TILE_SIZE, y*TILE_SIZE), tilesurface, [self.all_sprites], LAYERS['ground plant'])
    
        # for layer in ['randomveg']:
        # 	for x, y, tilesurface in tmx.get_layer_by_name(layer).tiles():
        # 		Generic((x*TILE_SIZE, y*TILE_SIZE), tilesurface, [self.all_sprites])
        for obj in tmx.get_layer_by_name('trees'):
            Tree((obj.x * 4, obj.y * 4), obj.image.convert_alpha(), [self.all_sprites, self.tree_sprites], obj.name, playeraddfunc = self.player_add)
   
        for obj in tmx.get_layer_by_name('smallveg'):
            Wildflower((obj.x * 4, obj.y * 4), obj.image.convert_alpha(), [self.all_sprites])
    
        for x, y, tilesurface in tmx.get_layer_by_name('collisions').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
   
        for obj in tmx.get_layer_by_name('player'):
            if obj.name == 'bed':
                Interaction(pos=(obj.x*4, obj.y * 4), size=(obj.width, obj.height), groups=self.interaction_sprites, name=obj.name)
             
        self.player = Player((640, 360),
                             self.all_sprites, 
                             self.collision_sprites,
                             self.tree_sprites,
                             self.soil_layer,
                             self.interaction_sprites,
                             self.toggle_shop,
                             self.toggles)
    
        Generic(pos= (0,0),
            surface = pygame.image.load('graphics/field.png').convert_alpha(),
              group=self.all_sprites, 
              z = LAYERS['ground'])
  
    def player_add(self, item):
        self.player.item_inventory[item] += 1
        self.success.play()
  
    def toggle_shop(self):
        self.shop_active = not self.shop_active
    
    def toggle_menu(self):
        self.menuactives[MENUS['help']] = not self.menuactives[MENUS['help']]
    
    def toggle_info(self):
        self.menuactives[MENUS['info']] = not self.menuactives[MENUS['info']]
    
    def toggle_credits(self):
        self.menuactives[MENUS['credits']] = not self.menuactives[MENUS['credits']]
        
    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestready and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    
                    row = plant.rect.centerx // TILE_SIZE
                    col = plant.rect.centery // TILE_SIZE
                    self.soil_layer.grid[col][row].remove('P')
    
    def reset(self):
        self.soil_layer.update_plants()
        
        self.soil_layer.remove_water()
        
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()
            
    def run(self,dt):
        self.display_surface.fill('black')
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.cameradraw(self.player)
        
        if self.shop_active:
            self.menu.update()
            
        elif True in self.menuactives:
            for i, menu in enumerate(self.menus):
                if self.menuactives[i] == True:
                    menu.show_menu()
            
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
  
        self.overlay.display()
        
        if self.player.sleep:
            self.transition.play()
        # print(self.player.item_inventory)
  
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.ground = pygame.image.load('graphics/field.png')
        self.groundwidth = self.ground.get_width() * 4
        self.groundheight = self.ground.get_height() * 4
        
    def cameradraw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        # print('before', self.offset)
        if self.offset.x < 0:
            self.offset.x = 0
        elif self.offset.x > self.groundwidth - SCREEN_WIDTH:
            self.offset.x = self.groundwidth - SCREEN_WIDTH
            
        if self.offset.y < 0:
            self.offset.y = 0
        elif self.offset.y > self.groundheight - SCREEN_HEIGHT:
            self.offset.y = self.groundheight - SCREEN_HEIGHT
        # print('after', self.offset)
            
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
                    
                    if sprite == player:
                        # pygame.draw.rect(self.display_surface,'red',offset_rect,5)
                        # hitbox_rect = player.hitbox.copy()
                        # hitbox_rect.center = offset_rect.center
                        # pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pygame.draw.circle(self.display_surface,'deepskyblue4',target_pos,5)

                