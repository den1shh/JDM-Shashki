import random
import pygame
import yaml
import pandas as pd
from modules.jdm_world import World
from modules.jdm_objects import Road, MyCar, TrafficCar

def load_cars():
    with open("configs/cars.yaml", "r") as file:
        confs = yaml.safe_load(file)
        cars = dict()
        for conf in confs:
            cars[conf['type']] = conf
        for car in cars.values():
            car['image'] = pygame.image.load('img/' + car['image'])
            car['image'] = pygame.transform.scale(car['image'], (car['width'], car['length']))
        return cars        
    
def crash(my_car, traffic_cars, world):
    sound = pygame.mixer.Sound('sounds/crash.wav')
    for car in traffic_cars:
        if car.rect.colliderect(my_car.rect):
            print('Game over')
            sound.play()
            world.game_status = False

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 800))
    background_color = (0, 0, 0)
    pygame.display.set_caption('Traffic racer')
    sound = pygame.mixer.Sound('sounds/engine.wav')
    sound.play(-1)
    font = pygame.freetype.Font(None, 20)

    spawn_road_time = pygame.USEREVENT
    pygame.time.set_timer(spawn_road_time, 850)
    spawn_traffic_time = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_traffic_time, 1000)

    cars = load_cars()
    my_car = MyCar((300, 600), cars['mercedes']['image'])

    road_image = pygame.image.load('img/road.png')
    road_image = pygame.transform.scale(road_image, (500, 800))
    world = World(my_car = my_car, roads = [Road(road_image, (250, 400)), Road(road_image, (250, -400)), Road(road_image, (250, -1200))])
    
    while world.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                world.alive = False
            if event.type == spawn_road_time:
                world.spawn_road(road_image)
            if event.type == spawn_traffic_time:
                world.spawn_traffic(cars)

        screen.fill(background_color)
        if world.game_status:
            my_car.move()
            world.draw_all(screen, my_car)
            crash(my_car, world.traffic_cars, world)
        else:
            font.render_to(screen, (30, 300), 'Game Over', (255, 255, 255))
            sound.stop()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

