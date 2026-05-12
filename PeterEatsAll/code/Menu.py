#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

EVENT_TIMEOUT = pygame.USEREVENT + 1

class Menu:
    def __init__(self, window):
        self.window = window
        # Load menu background
        self.surf = pygame.image.load('PeterEatsAll/asset/menu/menu-bg.jpg')
        # Draw a rectangle for the image
        self.rect = self.surf.get_rect(left=0, top=0)
        self.update_time = 1000

        pygame.time.set_timer(EVENT_TIMEOUT, 100)

    def run(self):
        menu_option = 0
        # Menu music
        pygame.mixer_music.load('PeterEatsAll/asset/menu/smolblackcat-lotus.mp3')
        pygame.mixer_music.play(-1) # -1 for looping
        pygame.mixer_music.set_volume(0.2)
        
        # How to play
        # 431, 195 / 430, 195
        # 794 460 pos
        htp = []
        htp.append(pygame.image.load('PeterEatsAll/asset/menu/how-to-play.png'))
        htp.append(pygame.image.load('PeterEatsAll/asset/menu/how-to-play2.png'))
        
        HTP_POS = (794, 460)
        # Texts
        play = pygame.image.load('PeterEatsAll/asset/menu/play.png')
        play_width = play.get_rect().width
        play_height = play.get_rect().height

        levels = pygame.image.load('PeterEatsAll/asset/menu/levels.png')
        levels_width = levels.get_rect().width
        levels_height = levels.get_rect().height

        options = pygame.image.load('PeterEatsAll/asset/menu/options.png')
        options_width = options.get_rect().width
        options_height = options.get_rect().height
        
        # Select options images
        fork = pygame.image.load('PeterEatsAll/asset/menu/menu-fork.png')
        spoon = pygame.image.load('PeterEatsAll/asset/menu/spoon.png')
        knife = pygame.image.load('PeterEatsAll/asset/menu/knife.png')

        # Scale 
        play = pygame.transform.smoothscale(play, (play_width * 0.3, play_height * 0.3))
        levels = pygame.transform.smoothscale(levels, (levels_width * 0.3, levels_height * 0.3))
        options = pygame.transform.smoothscale(options, (options_width * 0.3, options_height * 0.3))

        current_sprite = 0
       
        while True:
            # Draw menu image onto rectangle
            self.window.blit(source=self.surf, dest=self.rect)
            # Set text
            # self.menu_text(text_size=50, text="play", text_color=(255, 127, 87), text_center_pos=((1280 / 2), 50))
            if menu_option == 1:
                self.window.blit(fork, (475, 412))
            elif menu_option == 2:
                self.window.blit(spoon, (475, 494))
            elif menu_option == 3:
                self.window.blit(knife, (475, 580))
             
            # Draw menu texts 
            self.window.blit(play, (590, 430))
            self.window.blit(levels, (558, 510))
            self.window.blit(options, (550, 590))

            self.window.blit(htp[current_sprite], HTP_POS)

            if self.update_time <= 0:
                current_sprite += 1
                self.update_time = 1000
                if current_sprite >= len(htp):
                    current_sprite = 0

            # Update screen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == EVENT_TIMEOUT:
                    self.update_time -= 150
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s: # KEY DOWN
                        if menu_option == 3:
                            menu_option = 1
                        else:
                            menu_option += 1
                    if event.key == pygame.K_UP or event.key == pygame.K_w: # KEY UP
                        if menu_option == 1:
                            menu_option = 3
                        else:
                            menu_option -= 1
                    if event.key == pygame.K_RETURN: # ENTER
                        return menu_option
                
                        
                    

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
    
    
        pass
