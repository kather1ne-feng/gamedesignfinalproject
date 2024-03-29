import pygame
from util import *
from support import *
from timer import Timer
from plantinfo import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collisiongroup, treegroup, soillayer, interactionlayer, smallveg, toggle_shop, menutoggles, plant_toggle):
        super().__init__(group)
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        
        self.collision_sprites = collisiongroup
        self.hitbox = self.rect.copy().inflate((-126, -70))

        self.timers = {
            'tool_use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seeds),
            'seed switch': Timer(200)
        }
        
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]
        
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        
        self.tree_sprites = treegroup
        self.smallveg_sprites = smallveg
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
        
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }
        
        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
        }
        
        self.money = 200
        
        self.soil_layer = soillayer
        self.interaction_layer = interactionlayer
        self.sleep = False
        
        self.toggle_shop = toggle_shop
        self.toggles = menutoggles
    
        self.plant_toggle = plant_toggle
        self.plantinfo = PlantInfo('beautyberry', self.plant_toggle)
        
        self.watering = pygame.mixer.Sound('audio/water.mp3')
        self.watering.set_volume(0.2)
 
    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
                
        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()
    
    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
        
    def use_seeds(self):
        if self.seed_inventory[self.selected_seed] > 0:
            planted = self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            if planted:
                self.seed_inventory[self.selected_seed] -= 1
    
    def import_assets(self):
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                           'right_idle': [], 'left_idle': [], 'up_idle':[],
                           'down_idle': [], 'right_hoe': [], 'left_hoe': [],
                           'down_hoe':[], 'up_hoe':[], 'right_axe':[], 'left_axe': [],
                           'up_axe': [], 'down_axe':[], 'right_water': [],
                           'left_water': [], 'up_water': [], 'down_water':[]}
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            
        self.image = self.animations[self.status][int(self.frame_index)]
   
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['tool_use'].active and not self.timers['seed use'].active and not self.sleep:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'

            else:
                self.direction.y = 0
                
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'

            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'

            else:
                self.direction.x = 0
                
            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index = (self.tool_index + 1) % len(self.tools)
                self.selected_tool = self.tools[self.tool_index]
            
            if keys[pygame.K_s]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                # print('use seed')
            
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index = (self.seed_index + 1) % len(self.seeds)
                self.selected_seed = self.seeds[self.seed_index]
                # print(self.selected_seed)  
                
            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction_layer, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'bed':
                        self.status='left_idle'
                        self.sleep = True
                        
                for tree in self.tree_sprites.sprites():
                    if tree.rect.collidepoint(self.target_pos):
                        if tree.name == 'Small':
                            name = 'beautyberry'
                        else:
                            name = 'buckthorn'
                        self.plantinfo = PlantInfo(name, self.plant_toggle)
                        self.plantinfo.show_menu()
                for plant in self.smallveg_sprites.sprites():
                    if plant.rect.collidepoint(self.target_pos):
                        name = plant.name
                        self.plantinfo = PlantInfo(name, self.plant_toggle)
                        self.plantinfo.show_menu()
                        
            if keys[pygame.K_h]:
                self.toggles[MENUS['help']]()
            
            if keys[pygame.K_i]:
                self.toggle_shop()
                
            if keys[pygame.K_p]:
                self.toggles[MENUS['info']]()
            
            if keys[pygame.K_c]:
                self.toggles[MENUS['credits']]()
                
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
            
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                        
    def move(self, dt):
        # normalizing a vector 
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
            
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        
        self.move(dt)
        self.animate(dt)