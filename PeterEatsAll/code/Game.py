#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Menu import Menu
from code.Level import Level

EVENT_TIMEOUT = pygame.USEREVENT + 1

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        self.update_time = 1000
        self.show_keys = 4000
    
        pygame.time.set_timer(EVENT_TIMEOUT, 100)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        winning_image = pygame.image.load('PeterEatsAll/asset/game/winning-image.jpg')
        winning_image_rect = winning_image.get_rect()

        caught_image = pygame.image.load('PeterEatsAll/asset/game/caught.jpg')
        caught_image_rect = caught_image.get_rect()

        timeout_image = pygame.image.load('PeterEatsAll/asset/game/timeout.jpg')
        timeout_image_rect = timeout_image.get_rect()

        gameover = []
        gameover.append(pygame.image.load('PeterEatsAll/asset/game/gameover1.png'))
        gameover.append(pygame.image.load('PeterEatsAll/asset/game/gameover2.png'))
        gameover_rect = gameover[0].get_rect()

        youwon = []
        youwon.append(pygame.image.load('PeterEatsAll/asset/game/youwon1.png'))
        youwon.append(pygame.image.load('PeterEatsAll/asset/game/youwon2.png'))
        youwon_rect = youwon[0].get_rect()

        keys = []
        keys.append(pygame.image.load('PeterEatsAll/asset/game/keys.png'))
        keys.append(pygame.image.load('PeterEatsAll/asset/game/keys2.png'))
        keys_rect = keys[0].get_rect()
        
        on_game = False
        on_menu = True

        current_sprite = 0
        while running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        on_game = True
                        self.show_keys = 4000
                    elif event.key == pygame.K_BACKSPACE:
                        on_menu = True
                if event.type == EVENT_TIMEOUT:
                    self.update_time -= 100
                    self.show_keys -= 100

            if on_menu:
                menu = Menu(self.window)
                menu_return = menu.run()

                if menu_return == 1:
                    on_game = True
                    on_menu = False
                else:
                    continue

            if on_game:
                level = Level(self.window)
                levelreturn = level.run()
            
        
            if levelreturn != None:
                on_game = False
                self.window.fill("purple")
                
                if levelreturn == "won":
                    self.window.blit(winning_image, winning_image_rect)


                elif levelreturn == "caught":
                    self.window.blit(caught_image, caught_image_rect)
                    self.window.blit(keys[current_sprite], keys_rect) 

                elif levelreturn == "timeout":
                    self.window.blit(timeout_image, timeout_image_rect)      

                if self.show_keys <= 0:
                    self.window.blit(keys[current_sprite], keys_rect)  
                    self.show_keys = 0   

                    if levelreturn == "won":
                        self.window.blit(youwon[current_sprite], youwon_rect) 
                    else:
                        self.window.blit(gameover[current_sprite], gameover_rect) 
                    
            if self.update_time <= 0:
                current_sprite += 1
                self.update_time = 1000
                if current_sprite >= len(keys):
                    current_sprite = 0

  


            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60



        pygame.quit()
