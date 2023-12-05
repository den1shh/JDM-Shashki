import pygame
from typing import List
from jdm_objects import Object
from jdm_objects import Car

def car_hittest(body: Object, cars_objects: List[Object]):
    for obj in cars_objects:
        if body == obj or obj.alive == 0:
            continue
        col = pygame.sprite.collide_rect(body, obj)
        if col == True:
            sys.exit()

def move(self):
    """движение пушки по стрелочкам"""
    keys = pygame.key.get_pressed()
    if self.x <= 780:
        if keys[pygame.K_d]:
            self.x += 5
    if self.x >= 20:
        if keys[pygame.K_a]:
            self.x -= 5