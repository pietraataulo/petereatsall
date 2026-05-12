#!/usr/bin/python
# -*- coding: utf-8 -*-

# from Entity import Entity
import pygame.image

class Peter():
    def __init__(self):
        self.normal = []
        self.normal.append(pygame.image.load("PeterEatsAll/asset/peter/peter1.png").convert_alpha())
        self.normal.append(pygame.image.load("PeterEatsAll/asset/peter/peter2.png").convert_alpha())

        self.attacking = []
        self.attacking.append(pygame.image.load("PeterEatsAll/asset/peter/peter-attacking1.png").convert_alpha())
        self.attacking.append(pygame.image.load("PeterEatsAll/asset/peter/peter-attacking2.png").convert_alpha())

        self.current_sprite = 0
        self.image = self.normal[self.current_sprite]
        self.rect = self.image.get_rect()

    def update(self):
        self.current_sprite += 1

        if self.current_sprite >= len(self.normal):
            self.current_sprite = 0

        self.image = self.normal[self.current_sprite]
            
    def attack(self):
        if self.current_sprite >= len(self.attacking):
            self.current_sprite = 0
            
        self.image = self.attacking[self.current_sprite]
        pass
