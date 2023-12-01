import pygame as pg
import pygame.draw
import pygame.locals

from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

def get_car_image(file, size):
    image = pygame.image.load()
    image = pygame.transform.scale(image, size)
    return image

car_image = get_car_image('supra.png', (38, 90))