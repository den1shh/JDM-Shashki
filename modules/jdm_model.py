import pygame
from jdm_objects import Object
from jdm_objects import Car

def car_hittest(self, object):
    for obj in Car:
        if body == obj or obj.alive == 0:
            continue

def move(self):
    """движение пушки по стрелочкам"""
    keys = pygame.key.get_pressed()
    if self.x <= 780:
        if keys[pygame.K_d]:
            self.x += 5
    if self.x >= 20:
        if keys[pygame.K_a]:
            self.x -= 5