import pygame

def move(self):
    """движение пушки по стрелочкам"""
    keys = pygame.key.get_pressed()
    if self.x <= 780:
    if keys[pygame.K_RIGHT]:
        self.x += 5
        if self.x >= 20:
            if keys[pygame.K_LEFT]:
                    self.x -= 5