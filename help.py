import pygame
from util import *
from timer import Timer

class HelpMenu():
    def __init__(self, toggle_function):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('graphics/LycheeSoda.ttf', 30)
        self.toggle_function = toggle_function
        
        self.width = 800
        self.space = 5
        self.padding = 8
        
        self.options = ['Command Keys:',
                        'Q: Change Tool, rotates through hoe, axe, and watering can',
                        'Space: Use Tool, uses selected tool found in bottom left',
                        'E: Change Seed, rotates through corn or tomato seeds',
                        'S: Use Seed, plants a seed',
                        'Arrow Keys: Move around',
                        'Return/Enter: Sleep when in bed or buy/sell item in inventory',
                        'I: Open inventory',
                        'Escape: Exits current menu',
                        'P: Learn more about the game',
                        'C: See Game Credits'
        ]
        
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
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width /2, 
                                     self.menu_top, 
                                     self.width, 
                                     self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()
        
        if keys[pygame.K_ESCAPE]:
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
        

class GameInfo(HelpMenu):
    def __init__(self, toggle_info):
        super().__init__(toggle_info)
        self.width = 1000
        self.options = ['How To Play:',
                        'This game was made as a clone of Stardew Valley',
                        'The twist is that this version will teach you about restoration',
                        'Each day, you plant seeds, water your soil, and cut down trees',
                        'Each night, your plants grow and trees replenish',
                        'You can sell your items for money to buy more seeds',
                        'As you grow your plot of land, you can learn about native and invasive species',
                        'Along the way, you will also learn about restoration and biodiversity',
                        'Being near a tree and pressing enter can tell you about the species',
                        'Hope you enjoy!']
        self.setup()
        
class CreditMenu(HelpMenu):
    def __init__(self, toggle_info):
        super().__init__(toggle_info)
        self.width = 1000
        self.options = ['Game Credits:',
                        'I made this following a Youtube Tutorial,',
                        'Clear Code\'s "Creating a Stardew Valley inspired game in Python"',
                        'Literally huge thank you to his channel!!!!!!',
                        'I learned how to use Pygame, Tiled, and this entire project from him',
                        'Asset Pack by Cup Noodle: https://cupnooble.itch.io <333 for FREE!!!',
                        'Music: Original Soundtrack to "Stardew Valley" by ConcernedApe',
                        'https://concernedape.bandcamp.com/album/stardew-valley-ost']
        self.setup()