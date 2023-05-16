import pygame
from util import *
from timer import Timer

class PlantInfo():
    def __init__(self, name, toggle_function):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('graphics/LycheeSoda.ttf', 30)
        self.toggle_function = toggle_function
        
        self.width = 600
        self.space = 5
        self.padding = 8
        
        self.options = PLANT_INFO[name]
        
        self.timer = Timer(200)
        
        self.setup()
        
    def setup(self):
        self.text_surfs = []
        self.total_height = 0
        
        for i, item in enumerate(self.options):
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
            
        self.total_height += (len(self.text_surfs)-1) * self.space
        self.menu_top = SCREEN_HEIGHT - self.total_height - 20
        self.main_rect = pygame.Rect(SCREEN_WIDTH - self.width - 20, 
                                     self.menu_top, 
                                     self.width, 
                                     self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()
        
        if keys[pygame.K_RETURN]:
            self.toggle_function()
            
    def show_menu(self):
        self.input()
        pygame.draw.rect(self.display_surface, 'White', self.main_rect, 0, 10)
        top = self.main_rect.top 

        
        for i, text_surf in enumerate(self.text_surfs):
            bg_rect = pygame.Rect(self.main_rect.left + self.padding * 2, top, self.width, text_surf.get_height() + (self.padding * 2))        
            text_rect = text_surf.get_rect(midleft=(self.main_rect.left + self.padding * 2, bg_rect.centery))
            self.display_surface.blit(text_surf, text_rect)
            top += (text_surf.get_height() + (self.padding * 2) + self.space)