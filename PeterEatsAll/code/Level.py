#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from pygame.font import Font
from pygame import Surface, Rect
from code.Mintaka import Mintaka
from code.Peter import Peter
from code.Entity import Entity
import pygame.image
import math

EVENT_TIMEOUT = pygame.USEREVENT + 1

def linear_interpolation(x, x1, y1, x2, y2):
    return(x + x1) * ((y2 - y1) / (x2 - x1))

class Level:
    def __init__(self, window):
        self.window = window
        self.timeout = 30000 # game time
        self.update_time = 1000 # time to update sprite
        self.distracted_timer = 0 # mintakas distraction time
        self.change_action = 3000 # time to change action
        self.surf = pygame.image.load('PeterEatsAll/asset/game/bg-blue3.jpg')
        self.rect = self.surf.get_rect(left=0, top=0)

        self.turns = 0
        
        pygame.time.set_timer(EVENT_TIMEOUT, 100)


    def run(self):
        # Creating Mintaka and Peter
        mintaka = Mintaka()
        peter = Peter()

        PETER_ATK_POS = (286, 183)
        PETER_POS = (178, 260)
        pos = PETER_POS
        # tamanho 532, 455

        # Loading orange kitchen
        orange_kitchen = pygame.image.load('PeterEatsAll/asset/game/bg-orange3.jpg')
        orange_kitchen_rect = orange_kitchen.get_rect()

        # Loading winning image
        winning_image = pygame.image.load('PeterEatsAll/asset/game/winning-image.jpg')
        winning_image_rect = winning_image.get_rect()

        # Loading progress bar
        progress_bar = pygame.image.load('PeterEatsAll/asset/game/progress-bar.png')
        progress_bar_rect = progress_bar.get_rect()

        # Music
        attack_theme = 'PeterEatsAll/asset/game/peter-attacks.ogg'
        level_theme = 'PeterEatsAll/asset/game/smolblackcat-end.mp3'

        mintaka_song_file = 'PeterEatsAll/asset/mintaka/mintaka-song.ogg'
        mintaka_song = pygame.mixer.Sound(mintaka_song_file)
        mintaka_song.set_volume(0.027)

        current_theme = level_theme
        pygame.mixer_music.load(current_theme)
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)


        clock = pygame.time.Clock()
        screen_size = (1280, 720)
        BLUE = (0, 0, 255)
        
        RADIUS_INIT = 0
        RADIUS_FINAL = math.sqrt((screen_size[0]/2)**2 + (screen_size[1])**2)
        N_STEPS = 500
   
        step = 0
        current_step = 0

        clicking = False
        can_be_distracted = False

        bar_direction = 0
        RECT_Y = 65.8
        RECT_X = 495
        rect_width = 1
        bar_speed = 0.8

        rgb = [240, 187, 50]
        # (60, 187, 230)

        action = 4 # action number 
        sprites = mintaka.cooking 
        cooking = True
        direction = 1 # direction of turning sprites index
        singing = False
  
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    clicking = True
                    if current_step < 0:
                        current_step = 0
                    step = 5
                    bar_direction = 1
                    bar_speed = 0.8
  
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if current_step >= 500:
                        current_step = 499
                
                    clicking = False
                    step = -15

                    bar_direction = -1
                    bar_speed = 0.26

                if event.type == EVENT_TIMEOUT:
                    self.timeout -= 100
                    self.update_time -= 150
                    self.change_action -= 100
                    if self.timeout == 0:
                        pygame.mixer_music.load('PeterEatsAll/asset/game/smolblackcat-snowy.mp3')
                        pygame.mixer_music.set_volume(0.1)
                        pygame.mixer_music.play()
                        return "timeout"
                    if clicking:
                        if cooking or mintaka.image == mintaka.turning[0]:
                            # print(cooking)
                            # pygame.mixer_music.stop()
                            pygame.mixer_music.load('PeterEatsAll/asset/game/smolblackcat-snowy.mp3')
                            pygame.mixer_music.set_volume(0.1)
                            pygame.mixer_music.play()
                            return "caught"
                        elif rect_width >= 300:
                            pygame.mixer_music.set_volume(0.1)
                            return "won"

                    
            clock.tick(60)

            # Play themes
            new_theme = attack_theme if clicking else level_theme

            if new_theme != current_theme:
                    pygame.mixer_music.load(new_theme)
                    pygame.mixer_music.play(-1)
                    current_theme = new_theme

            
            self.window.blit(source=self.surf, dest=self.rect)

            canvas = pygame.surface.Surface(screen_size)
            canvas_rect = canvas.get_rect()
            canvas.blit(orange_kitchen, orange_kitchen_rect)
            
            if current_step >= 500:
                step = 0
            
            current_step += step + (clock.get_time() / 1000)
  
            radius = linear_interpolation(current_step, 0, RADIUS_INIT, N_STEPS, RADIUS_FINAL)
            
            # Draw circle
            pygame.draw.circle(canvas, BLUE, (screen_size[0]/2, screen_size[1]/2), radius)
        
            # Chroma key
            canvas.set_colorkey(BLUE)

            self.window.blit(canvas, canvas_rect)
            
            # Change rectangle width
            rect_width += bar_speed * bar_direction
            
            # Draw progress bar (rectangle)
            pygame.draw.rect(self.window, rgb, [RECT_X, RECT_Y, rect_width, 35], 0, 18)
            
            # Change progress bar color
            if rect_width < 1:
                bar_direction = 0
            elif rect_width >= 150:
                if rgb[0] > 1:
                    rgb[0] -= 2
                if rgb[2] < 254:
                    rgb[2] += 2
            elif rect_width <= 150:
                if rgb[0] < 254:
                    rgb[0] += 2
                if rgb[2] > 1:
                    rgb[2] -= 2

            # Draw progress bar
            self.window.blit(progress_bar, progress_bar_rect)

       
            # If Mintaka can be distracted but is still cooking, Mintaka turns around and gets distracted
            if can_be_distracted and action > 3:
                cooking = False
                direction = 1
                
                if self.turns < 2:
                    mintaka.turn(direction, self.turns)
                    sprites = mintaka.turning
                else:
                    self.turns = 0
                    action = random.randint(1, 3)

            else:
                can_be_distracted = self.get_distracted(action)
            
            # Distraction was chosen
            if action in [1, 2, 3]:
                # If distraction time is over, Mintaka turns around and cooks again
                if self.distracted_timer <= 0:
                    if self.turns < 2:
                        direction = -1
                        sprites = mintaka.turning
                    else:
                        self.change_action = 5000
                        self.turns = 0
                        sprites = mintaka.cooking
                        can_be_distracted = False
                        cooking = True
                        mintaka.current_sprite = 0
                        direction = 1
                        action = 4

                        if singing:
                            mintaka_song.stop()
                            singing = False
                else:
                    action_timer_speed = random.randrange(15, 21, 5)
                    self.distracted_timer -= action_timer_speed
                    match action:
                        case 1:
                            mintaka.play()
                            sprites = mintaka.playing
                        case 2:
                            mintaka.dance()
                            sprites = mintaka.dancing
                            if not singing:
                                mintaka_song.play(0)
                                singing = True
                        case 3:
                            mintaka.drink()
                            sprites = mintaka.drinking
   
            # playing pos 823, 127
            # peter pos 178 260
            # peter red 247 370
            # 390, 593 red
            if clicking:
                pos = PETER_ATK_POS
                peter.attack()
            else:
                pos = PETER_POS
                peter.image = peter.normal[peter.current_sprite]

            self.window.blit(mintaka.image, (849, 127))
            self.window.blit(peter.image, pos)

            # Switch to next sprite 
            if self.update_time <= 0:
                mintaka.update(sprites, direction, self.turns)
                peter.update()
                self.update_time = 1000

                if mintaka.image in mintaka.turning:      
                    self.turns += 1
     
            # Print timeout
            self.level_text(65, f'{self.timeout // 1000}', text_color=(232, 230, 255), text_center_pos=((screen_size[0] / 2 + 4), (screen_size[1] / 4.5 - 4)))

            pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="twcennegrito", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def get_distracted(self, act):
        # If distraction time is over
        if self.distracted_timer <= 0:
            # If its time to change action
            if self.change_action <= 0:
                # Python chooses a random number between 1, 2 and 3
                # If the number is 1, Mintaka can be distracted
                n = random.randint(1, 3)
                if n == 1 and act > 3:
                    # Reset timers
                    self.change_action = 3000
                    self.distracted_timer = 3000       
                    return True
                else:
                    return False


    
