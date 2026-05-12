#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.Entity import Entity
import pygame.image

class Mintaka(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cooking = []
        self.cooking.append(pygame.image.load("PeterEatsAll/asset/mintaka/cooking1-red.png").convert_alpha())
        self.cooking.append(pygame.image.load("PeterEatsAll/asset/mintaka/cooking2-red.png").convert_alpha())
        self.cooking.append(pygame.image.load("PeterEatsAll/asset/mintaka/cooking3-red.png").convert_alpha())
        self.cooking.append(pygame.image.load("PeterEatsAll/asset/mintaka/cooking2-red.png").convert_alpha())

        self.playing = []
        self.playing.append(pygame.image.load("PeterEatsAll/asset/mintaka/playing1-red.png").convert_alpha())
        self.playing.append(pygame.image.load("PeterEatsAll/asset/mintaka/playing2-red.png").convert_alpha())

        self.drinking = []
        self.drinking.append(pygame.image.load("PeterEatsAll/asset/mintaka/drinking1.png").convert_alpha())   
        self.drinking.append(pygame.image.load("PeterEatsAll/asset/mintaka/drinking2.png").convert_alpha())    

        self.dancing = []
        self.dancing.append(pygame.image.load("PeterEatsAll/asset/mintaka/dancing1.png").convert_alpha())
        self.dancing.append(pygame.image.load("PeterEatsAll/asset/mintaka/dancing2.png").convert_alpha())

        self.turning = []
        self.turning.append(pygame.image.load("PeterEatsAll/asset/mintaka/turning1.png").convert_alpha())
        self.turning.append(pygame.image.load("PeterEatsAll/asset/mintaka/turning2.png").convert_alpha())

        self.current_sprite = 0
        self.image = self.cooking[self.current_sprite]
        self.rect = self.image.get_rect()


    def update(self, sprites_list, direction, turns): 
        self.current_sprite += direction

        if direction == 1 and self.current_sprite >= len(sprites_list):
            if self.image in self.turning:
                return
            self.current_sprite = 0

        elif direction == -1 and turns == 0:
            self.current_sprite = len(sprites_list) - 1
        
        self.image = sprites_list[self.current_sprite]

    def turn(self, direction, turns):
        if direction == 1 and turns == 0:
            self.current_sprite = 0
        
        elif direction == -1 and turns == 0:
            self.current_sprite = len(self.turning) - 1

        self.image = self.turning[self.current_sprite]


    def play(self):
        if self.current_sprite >= len(self.playing):
            self.current_sprite = 0
        self.image = self.playing[int(self.current_sprite)]
        

    def drink(self):
        if self.current_sprite >= len(self.drinking):
            self.current_sprite = 0
        self.image = self.drinking[int(self.current_sprite)]
     
    def dance(self):
        if self.current_sprite >= len(self.dancing):
            self.current_sprite = 0
        self.image = self.dancing[int(self.current_sprite)]
       
