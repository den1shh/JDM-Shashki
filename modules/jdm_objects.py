import pygame


class MyCar:
    """Класс машины игрока"""

    def __init__(self, position, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.game_status = "game"
        self.energy = 7

    def border(self):
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0

    def move(self):
        key = pygame.key.get_pressed()
        speed = 6
        if key[pygame.K_a]:
            self.rect.x -= speed
        if key[pygame.K_d]:
            self.rect.x += speed
        self.border()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, world):
        self.energy -= 0.01
        self.rect.y = 800 - self.energy * 30
        if self.rect.top > 820:
            world.game_status = False


class Item(pygame.sprite.Sprite):
    """Класс предмета на трассе, движещейся по ней с некой скоростью"""

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


class Petrol(Item):
    """Класс канистр бензина"""

    def __init__(self, energy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energy = energy
