import pygame
from util import * 
from random import randint, choice
from timer import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, group, z = LAYERS['main']):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*4), int(self.size[1]*4)))
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.2, -self.rect.height*0.75))
          
class Wildflower(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        self.z = LAYERS['ground plant']
        self.image = pygame.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))
        self.name = name
                
class Tree(Generic):    
    def __init__(self, pos, surf, group, name, playeraddfunc):
        super().__init__(pos, surf, group)
        
        self.name = name
        self.health = 5
        self.alive = True
        self.stump_surf = pygame.image.load(f'graphics/objects/stump_{"small" if name == "Small" else "medium"}.png').convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (int(self.size[0]), int(self.size[1])))

        
        self.apple_surface = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
        self.size = self.apple_surface.get_size()
        self.apple_surface = pygame.transform.scale(self.apple_surface, (int(self.size[0]/4), int(self.size[1]/4)))


        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()
        
        self.player_add = playeraddfunc
        
        self.axe_sound = pygame.mixer.Sound('audio/axe.mp3')
        
    def damage(self):
        self.health -=1
        self.axe_sound.play()
        
        if (len(self.apple_sprites.sprites()) > 0):
            random_apple = choice(self.apple_sprites.sprites())
            self.player_add('apple')
            random_apple.kill()
            
            
    def check_dead(self):
        if self.health <= 0:
            self.alive = False
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.player_add('wood')
            
    def update(self, dt):
        if self.alive:
            self.check_dead()     
               
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x, y), self.apple_surface, [self.apple_sprites, self.groups()[0]], LAYERS['fruit'])
                
class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name