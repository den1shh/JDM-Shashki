import pygame.sprite


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, image, position, speed):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def remove(self):
        if self.rect.top > 800:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.remove()
