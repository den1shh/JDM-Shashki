import pygame
import random
from modules.jdm_objects import MyCar, Item, Petrol

class World:
    def __init__(
            self,
            roads: list[Item],
            time: int = 0,
            choosed_track: str() = 'racetrack',
            ):
        self.alive = True
        self.game_status = True
        self.traffic_cars = pygame.sprite.Group()
        self.roads = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.petrols = pygame.sprite.Group()
        self.roads.add(roads)
        self.speed = 15
        self.time = time
        self.game_time = 0
        self.point = 0
        self.accel = 0.1
        if choosed_track == 'racetrack':
            self.cols = 4
        else:
            self.cols = 6

    def spawn_road(self, road_image):
        road = Item(road_image, (400, -800), self.speed)
        self.roads.add(road)

    def spawn_traffic(self, cars):
        position = (random.randint(50, 750), random.randint(-250, -200))
        speed = random.randint(self.speed - 5, self.speed - 1)
        traffic_car = Item(random.choice(list(cars.values()))['image'], position, speed)
        self.traffic_cars.add(traffic_car)

    def update_road(self, spawn_road_time):
        pygame.time.set_timer(spawn_road_time, int(400/self.speed/60*1000))

    def spawn_coin(self, coin_image):
        position = (random.choice([int(800/self.cols/2 + 800/self.cols*i) for i in range(self.cols)]), -40)
        coin = Item(coin_image, position, self.speed)
        self.coins.add(coin)

    def spawn_petrol(self, petrols):
        petrol = random.choice(list(petrols.values()))
        position = (random.randint(50, 750), random.randint(-250, -200))
        petrol = Petrol(petrol['energy'], petrol['image'], position, self.speed)
        self.petrols.add(petrol)


    def draw_all(self, screen):
        self.roads.update()
        self.roads.draw(screen)
        self.traffic_cars.update()
        self.traffic_cars.draw(screen)
        self.coins.update()
        self.coins.draw(screen)
        self.petrols.update()
        self.petrols.draw(screen)

    def acceleration(self, time):
        self.game_time += time - self.time
        self.speed = int(15 + self.game_time*self.accel/1000)
        self.time_sync(time)

    def time_sync(self, time):
        self.time = time