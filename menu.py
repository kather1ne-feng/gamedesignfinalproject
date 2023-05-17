import pygame
from util import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_shop):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('graphics/LycheeSoda.ttf', 30)
        self.toggle_shop = toggle_shop
        
        self.width = 400
        self.space = 10
        self.padding = 8
        
        seed_list = list(self.player.seed_inventory.keys())
        seed_list = [f'{seed} seeds' for seed in seed_list]
        self.options = list(self.player.item_inventory.keys()) + seed_list
        self.sell_index = len(self.player.item_inventory) - 1
        
        self.index = 0
        self.timer = Timer(200)
        
        self.setup()
        
    def setup(self):
        self.text_surfs = []
        self.total_height = 0
        
        for i, item in enumerate(self.options):
            item = item.split(' ')[0]
            itemstring = f'{item} - ${SALE_PRICES[item] if i <= self.sell_index else PURCHASE_PRICES[item]}'
            text_surf = self.font.render(itemstring, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
            
        self.total_height += (len(self.text_surfs)-1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width /2, 
                                     self.menu_top, 
                                     self.width, 
                                     self.total_height)
        
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH /2, SCREEN_HEIGHT - 20))
        
        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 10)
        self.display_surface.blit(text_surf, text_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()
        
        if keys[pygame.K_ESCAPE]:
            self.toggle_shop()
        
        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
                # self.index %= len(self.options)
                
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
                # self.index %= len(self.options)
            
            if keys[pygame.K_RETURN]:
                self.timer.activate()
                
                current_item = self.options[self.index]
                
                # print(self.index)
                # print(self.sell_index)
                if self.index <= self.sell_index:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]
                else:
                    item = current_item.split(' ')[0]
                    seed_price = PURCHASE_PRICES[item]
                    
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[item] += 1
                        self.player.money -= PURCHASE_PRICES[item]
                        
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) -1 :
            self.index = 0
            
    def show_entry(self, text_surf, amount, top, selected):
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 10)
        
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)
        
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)
        
        if selected:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect, 3, 10)
            if self.index <= self.sell_index:
                pos_rect = self.sell_text.get_rect(midleft=(self.main_rect.left + 225, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:
                pos_rect = self.buy_text.get_rect(midleft=(self.main_rect.left + 225, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)
                
    def update(self):
        self.input()
        # pygame.draw.rect(self.display_surface, 'red', self.main_rect)
        self.display_money()
        for textindex, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + textindex * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[textindex]
            self.show_entry(text_surf, amount, top, self.index == textindex)
            # self.display_surface.blit(text_surf, (100, textindex * 50))
        # self.display_surface.blit(pygame.Surface((1000, 1000)), (0,0))