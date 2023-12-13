import pygame
import random
from modules.jdm_objects import MyCar, Item

class World:
    def __init__(
            self,
            roads: list[Item],
            my_car: MyCar,
            ):
        self.alive = True
        self.game_status = True
        self.traffic_cars = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.roads.add(roads)
        self.speed = 15
        self.time = 0
        self.point = 0
        self.accel = 0.1

    def spawn_road(self, road_image):
        road = Item(road_image, (250, -600), self.speed)
        self.roads.add(road)

    def spawn_traffic(self, cars):
        position = (random.randint(40, 460), random.randint(-60, -40))
        speed = random.randint(self.speed - 5, self.speed - 1)
        traffic_car = Item(random.choice(list(cars.values()))['image'], position, speed)
        self.traffic_cars.add(traffic_car)

    def spawn_coin(self, coin_image):
        position = (random.choice([int(500/4/2 + 500/4*i) for i in range(4)]), -40)
        coin = Item(coin_image, position, self.speed)
        self.coins.add(coin)

    def draw_all(self, screen, my_car):
        self.roads.update()
        self.roads.draw(screen)
        self.traffic_cars.update()
        self.traffic_cars.draw(screen)
        self.coins.update()
        self.coins.draw(screen)
        my_car.draw(screen)

    def acceleration(self, time):
        self.time = time
        self.speed = int(15 + self.time*self.accel)