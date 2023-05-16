import pygame
from util import *
from pytmx.util_pygame import load_pygame
from random import choice
from support import *

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, spritegroup):
        super().__init__(spritegroup)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']
        
class WateredSoil(pygame.sprite.Sprite):
    def __init__(self, pos, surf, spritegroup):
        super().__init__(spritegroup)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']
 
class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, checkwatered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder_dict(f'graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = checkwatered
        
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestready = False
        
        self.image = self.frames[str(self.age)]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']
        
    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed
            
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestready = True
            
            self.image = self.frames[str(int(self.age))]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        
class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.watered_soil = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        
        self.soil_surface = pygame.image.load('graphics/o.png')
        self.water_surfaces = import_folder('graphics/soil_water')
        self.create_soil_grid()
        self.create_hit_rects()
        
        self.hoe_sound = pygame.mixer.Sound('audio/hoe.wav')
        self.hoe_sound.set_volume(0.1)
        
        self.plant_sound = pygame.mixer.Sound('audio/plant.wav')
        self.plant_sound.set_volume(0.1)
        
    def create_soil_grid(self):
        ground = pygame.image.load('graphics/field.png')
        widthtiles, heighttiles = ground.get_width() // 16, ground.get_height() // 16
        self.grid = [[[] for col in range(widthtiles)] for row in range(heighttiles)]
        for x, y, tile in load_pygame('field.tmx').get_layer_by_name('farmarea').tiles():
            self.grid[y][x].append('F')
    
    def create_hit_rects(self):
        self.hit_rects = []
        
        for rowindex, row in enumerate(self.grid):
            for colindex, cell in enumerate(row):
                if 'F' in cell:
                    x = colindex * TILE_SIZE
                    y = rowindex * TILE_SIZE
                    rect = pygame.Rect(x,y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)
                    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for rowindex, row in enumerate(self.grid):
            for colindex, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(pos=(colindex * TILE_SIZE, rowindex * TILE_SIZE),
                             surf=self.soil_surface,
                             spritegroup = [self.all_sprites, self.soil_sprites])
            
    def water(self, target_pos):
        for soil in self.soil_sprites.sprites():
            if soil.rect.collidepoint(target_pos):
                x = soil.rect.x // TILE_SIZE
                y = soil.rect.y // TILE_SIZE
                
                self.grid[y][x].append('W')
                WateredSoil(pos=soil.rect.topleft,
                            surf=choice(self.water_surfaces),
                            spritegroup=[self.all_sprites, self.watered_soil])
                
    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        iswatered = 'W' in cell
        return iswatered
    
    def plant_seed(self, target_pos, seed):
        for soil in self.soil_sprites.sprites():
            if soil.rect.collidepoint(target_pos):
                self.plant_sound.play()
                x = soil.rect.x // TILE_SIZE
                y = soil.rect.y // TILE_SIZE
                
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(seed, [self.all_sprites, self.plant_sprites], soil, self.check_watered)
                    
    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()
                    
    def remove_water(self):
        for sprite in self.watered_soil.sprites():
            sprite.kill()
            
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')