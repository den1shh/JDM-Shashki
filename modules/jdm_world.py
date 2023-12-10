import pygame
import random
from modules.jdm_objects import Road, MyCar, TrafficCar

class World:
    def __init__(
            self,
            roads: list[Road],
            my_car: MyCar,
            ):
        self.alive = True
        self.game_status = True
        self.traffic_cars = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()
        self.roads.add(roads)
        self.my_car = my_car

    def spawn_road(self, road_image):
        road = Road(road_image, (250, -600))
        self.roads.add(road)

    def spawn_traffic(self, cars):
        position = (random.randint(40, 460), random.randint(-60, -40))
        speed = random.randint(10, 15)
        traffic_car = TrafficCar(random.choice(list(cars.values()))['image'], position, speed)
        self.traffic_cars.add(traffic_car)

    def draw_all(self, screen, my_car):
        self.roads.update()
        self.roads.draw(screen)
        self.traffic_cars.update()
        self.traffic_cars.draw(screen)
        my_car.draw(screen)
