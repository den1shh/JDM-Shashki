import pygame as pg
import pygame.draw
import pygame.locals

import pygame_widgets

def get_car_image(file, size):
    image = pygame.image.load()
    image = pygame.transform.scale(image, size)
    return image

car_image = get_car_image('supra.png', (38, 90))